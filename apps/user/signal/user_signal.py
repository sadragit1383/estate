from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
from apps.user.models.user_model import UserSecret,UserLogin
from apps.user.models.wallet_model import Wallet, Currency


@receiver(post_save, sender=UserSecret)
def activate_user_wallet(sender, instance, **kwargs):
    """
    زمانی که کاربر تأیید شود، کیف پول برای او ساخته می‌شود.
    """
    if instance.isActive and instance.isVerfied:
        wallet, created = Wallet.objects.get_or_create(
            userId=instance.user,
            defaults={
                'balance': 0,
                'currency': Currency.objects.filter(isActive=True).first()
            }
        )
        if created:
            print(f"کیف پول جدید برای {instance.user.mobileNumber} ایجاد شد.")
        else:
            print(f"کیف پول برای {instance.user.mobileNumber} از قبل موجود است.")



@receiver(pre_save, sender=UserSecret)
def handle_user_ban_status(sender, instance, **kwargs):
    """
    سیگنال برای همگام‌سازی وضعیت بلاک بودن کاربر در تمام مدل‌های مرتبط
    """
    if instance.pk:
        try:
            old_instance = UserSecret.objects.get(pk=instance.pk)

            if old_instance.isBan != instance.isBan:
                user = instance.user
                is_banned = instance.isBan

                # تنظیم مقادیر در UserSecret
                instance.isActive = not is_banned
                instance.isVerfied = not is_banned

                Wallet.objects.filter(userId=user).update(isActive=not is_banned)

        except UserSecret.DoesNotExist:
            pass