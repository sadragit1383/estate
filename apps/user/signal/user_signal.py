from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.user.models.user_model import User,UserSecret
from apps.user.models.wallet_model import Wallet, Currency


@receiver(post_save, sender=User)
def activate_user_wallet(sender, instance, **kwargs):
    """
    هنگامی که کاربر فعال و تایید شده باشد، کیف پول او فعال‌سازی می‌شود.
    """
    try:
        user_secret = instance.usersecret
        if user_secret.isActive and user_secret.isVerified:
            wallet, created = Wallet.objects.get_or_create(
                user=instance,
                isActive=True,
                defaults={
                    'balance': 0,
                    'currency': Currency.objects.filter(isActive=True).first()
                }
            )
            if created:
                print(f"کیف پول جدید برای {instance.mobileNumber} ایجاد شد.")
            else:
                print(f"کیف پول {instance.mobileNumber} فعال و موجودیت فعلی بررسی شد.")
    except UserSecret.DoesNotExist:
        print(f"UserSecret برای {instance.mobileNumber} یافت نشد.")
