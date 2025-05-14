from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.user.models.user_model import User
from apps.user.models.wallet_model import Wallet, Currency


@receiver(post_save, sender=User)
def activate_user_wallet(sender, instance, **kwargs):
    """
    هنگامی که کاربر فعال و تایید شده باشد، کیف پول او فعال‌سازی می‌شود.
    """
    if instance.isActive and instance.isVerified:
        # بررسی کیف پول کاربر
        wallet, created = Wallet.objects.get_or_create(
            user=instance,
            isActive=True,  # کیف پول فعال
            defaults={
                'balance': 0,  # موجودی اولیه صفر
                'currency': Currency.objects.filter(isActive=True).first()  # ارز فعال اول
            }
        )
        if created:
            print(f"کیف پول جدید برای {instance.mobileNumber} ایجاد شد.")
        else:
            print(f"کیف پول {instance.mobileNumber} فعال و موجودیت فعلی بررسی شد.")
