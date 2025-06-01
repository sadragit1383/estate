from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from apps.user.models.user_model import RoleUser, User
from ..models.agency_model import Agency, RejectedAgency

@receiver(pre_save, sender=Agency)

def update_user_role_on_agency_status_change(sender, instance, **kwargs):
    if not instance.user:
        return  # اگر کاربر ندارد، ادامه نده

    # اگر آژانس قبلاً وجود داشته باشد
    if instance.pk:
        old_agency = Agency.objects.filter(pk=instance.pk).first()

        if old_agency and old_agency.status != instance.status:
            # اگر وضعیت جدید فعال است
            if instance.status == Agency.Status.ACTIVE:
                agency_role, _ = RoleUser.objects.get_or_create(
                    slug='agency',
                    defaults={'title': 'Agency', 'isActive': True}
                )
                instance.user.role = agency_role
                instance.user.save()

            # اگر وضعیت جدید رد شده است
            elif instance.status == Agency.Status.REJECTED:
                user_role, _ = RoleUser.objects.get_or_create(
                    slug='user',
                    defaults={'title': 'User', 'isActive': True}
                )
                instance.user.role = user_role
                instance.user.save()
    else:
        # اگر آژانس جدید است و وضعیت فعال دارد
        if instance.status == Agency.Status.ACTIVE:
            agency_role, _ = RoleUser.objects.get_or_create(
                slug='agency',
                defaults={'title': 'Agency', 'isActive': True}
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