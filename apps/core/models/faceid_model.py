from django.db import models
from user.models import User
import uuid


class FaceVerificationStatus(models.TextChoices):
    PENDING = 'pending', 'در انتظار تایید'
    VERIFIED = 'verified', 'تایید شده'
    REJECTED = 'rejected', 'رد شده'
    EXPIRED = 'expired', 'منقضی شده'

class FaceImage(models.Model):

    """
    ذخیره تصاویر چهره کاربران برای تشخیص هویت
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='faceImages')
    image = models.ImageField(upload_to='faceVerification/')
    createdAt = models.DateTimeField(auto_now_add=True)
    isActive = models.BooleanField(default=True)

    # ویژگی‌های استخراج شده از چهره (برای مقایسه بعدی)
    faceEncoding = models.BinaryField(null=True, blank=True)

    class Meta:
        db_table = 'user_face_images'
        verbose_name = 'تصویر چهره'
        verbose_name_plural = 'تصاویر چهره'


class FaceVerificationRequest(models.Model):
    """
    درخواست‌های احراز هویت با چهره
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sessionKey = models.CharField(max_length=255)  # برای مدیریت session
    status = models.CharField(
        max_length=20,
        choices=FaceVerificationStatus.choices,
        default=FaceVerificationStatus.PENDING
    )
    createdAt = models.DateTimeField(auto_now_add=True)
    expiresAt = models.DateTimeField()  # زمان انقضای درخواست
    attemptCount = models.PositiveIntegerField(default=0)  # تعداد تلاش‌ها

    # اطلاعات فنی
    ipAddress = models.CharField(max_length=45)
    userAgent = models.TextField()


    class Meta:
        db_table = 'user_face_verification_requests'
        verbose_name = 'درخواست احراز چهره'
        verbose_name_plural = 'درخواست‌های احراز چهره'


class FaceVerificationLog(models.Model):

    """
    لاگ‌های عملیات احراز هویت چهره
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    request = models.ForeignKey(FaceVerificationRequest, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    success = models.BooleanField()
    confidence = models.FloatField(null=True)  # میزان اطمینان از تطابق
    image = models.ForeignKey(FaceImage, on_delete=models.SET_NULL, null=True)


    class Meta:
        db_table = 'user_face_verification_logs'
        verbose_name = 'لاگ احراز چهره'
        verbose_name_plural = 'لاگ‌های احراز چهره'