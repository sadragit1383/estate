from django.utils import timezone
from django.core.exceptions import ValidationError
from ..models.advertisement import Advertisement, SecretAdvertisement

class AdvertisementService:
    @staticmethod
    def renew_advertisement(advertisement_id: int, days: int = 30) -> Advertisement:
        """
        تمدید آگهی به مدت روزهای مشخص
        :param advertisement_id: آیدی آگهی
        :param days: تعداد روزهای تمدید (پیش‌فرض 30 روز)
        :return: آگهی به‌روزرسانی شده
        """
        try:
            advertisement = Advertisement.objects.get(pk=advertisement_id)
            secret = SecretAdvertisement.objects.get(advertisement=advertisement)

            # تمدید تاریخ انقضا
            advertisement.expired_at = timezone.now() + timezone.timedelta(days=days)
            advertisement.save()

            # به‌روزرسانی وضعیت تمدید
            secret.isRenewal = True
            secret.save()

            return advertisement
        except Advertisement.DoesNotExist:
            raise ValidationError("آگهی مورد نظر یافت نشد")

    @staticmethod
    def flag_advertisement(advertisement_id: int, reason: str = None) -> SecretAdvertisement:
        """
        علامت‌گذاری آگهی به عنوان مشکوک
        :param advertisement_id: آیدی آگهی
        :param reason: دلیل علامت‌گذاری (اختیاری)
        :return: وضعیت مخفی آگهی
        """
        try:
            advertisement = Advertisement.objects.get(pk=advertisement_id)
            secret, created = SecretAdvertisement.objects.get_or_create(
                advertisement=advertisement,
                defaults={'isFlagged': True}
            )

            if not created:
                secret.isFlagged = True
                secret.save()

            # در اینجا می‌توانید reason را در یک مدل جداگانه ذخیره کنید
            return secret
        except Advertisement.DoesNotExist:
            raise ValidationError("آگهی مورد نظر یافت نشد")

    @staticmethod
    def mark_info_completed(advertisement_id: int) -> SecretAdvertisement:
        """
        علامت‌گذاری آگهی به عنوان تکمیل اطلاعات
        :param advertisement_id: آیدی آگهی
        :return: وضعیت مخفی آگهی
        """
        try:
            advertisement = Advertisement.objects.get(pk=advertisement_id)
            secret, created = SecretAdvertisement.objects.get_or_create(
                advertisement=advertisement,
                defaults={'isInfoCompleted': True}
            )

            if not created:
                secret.isInfoCompleted = True
                secret.save()

            return secret
        except Advertisement.DoesNotExist:
            raise ValidationError("آگهی مورد نظر یافت نشد")