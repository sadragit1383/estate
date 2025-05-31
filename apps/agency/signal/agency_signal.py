from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from apps.user.models.user_model import RoleUser, User
from ..models.agency_model import Agency, RejectedAgency

@receiver(pre_save, sender=Agency)
def update_user_role_on_agency_status_change(sender, instance, **kwargs):
    """
    سیگنال برای تغییر نقش کاربر هنگام تغییر وضعیت آژانس
    - وقتی آژانس تایید می‌شود: نقش کاربر به agency تغییر می‌کند
    - وقتی آژانس رد می‌شود: نقش کاربر به user تغییر می‌کند
    """
    if instance.pk:  # اگر آژانس از قبل وجود دارد
        old_agency = Agency.objects.get(pk=instance.pk)

        # اگر وضعیت تغییر کرده است
        if old_agency.status != instance.status:
            # حالت تایید آژانس
            if instance.status == Agency.Status.ACTIVE:
                agency_role, created = RoleUser.objects.get_or_create(
                    slug='agency',
                    defaults={
                        'title': 'Agency',
                        'isActive': True
                    }
                )
                instance.user.role = agency_role
                instance.user.save()

            # حالت رد آژانس
            elif instance.status == Agency.Status.REJECTED:
                user_role, created = RoleUser.objects.get_or_create(
                    slug='user',
                    defaults={
                        'title': 'User',
                        'isActive': True
                    }
                )
                instance.user.role = user_role
                instance.user.save()
    else:
        # برای آژانس جدید
        if instance.status == Agency.Status.ACTIVE:
            agency_role, created = RoleUser.objects.get_or_create(
                slug='agency',
                defaults={
                    'title': 'Agency',
                    'isActive': True
                }
            )
            instance.user.role = agency_role
            instance.user.save()


@receiver(post_save, sender=RejectedAgency)
def update_user_role_on_rejection(sender, instance, created, **kwargs):
    """
    سیگنال برای تغییر نقش کاربر به user وقتی آژانس رد می‌شود
    (به عنوان یک مکانیزم پشتیبان)
    """
    if created:
        user_role, created = RoleUser.objects.get_or_create(
            slug='user',
            defaults={
                'title': 'User',
                'isActive': True
            }
        )
        instance.agency.user.role = user_role
        instance.agency.user.save()