from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
import uuid
from apps.user.models.user_model import User
from .agency_model import Agency
from apps.user.models.validation.user_validation import CleanFieldsMixin


class Role(models.TextChoices):
    MANAGER = 'manager', 'مدیر'
    CONSULTANT = 'consultant', 'مشاور'
    ADMIN = 'admin', 'ادمین'


class StatusResponse(models.TextChoices):
    PENDING = 'pending', 'در انتظار بررسی'
    ACCEPTED = 'accepted', 'تایید شده'
    REJECTED = 'rejected', 'رد شده'
    CANCELLED = 'cancelled', 'لغو شده'


class RequestCollaborationAgency(CleanFieldsMixin,models.Model):

    """
    مدل برای مدیریت درخواست‌های همکاری با آژانس‌های املاک
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name='شناسه یکتا'
    )

    agency = models.ForeignKey(
        Agency,
        on_delete=models.CASCADE,
        related_name='collaboration_requests',
        verbose_name='آژانس'
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='agency_requests',
        verbose_name='کاربر درخواست دهنده'
    )

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.CONSULTANT,
        verbose_name='نقش درخواستی'
    )

    status = models.CharField(
        max_length=20,
        choices=StatusResponse.choices,
        default=StatusResponse.PENDING,
        verbose_name='وضعیت درخواست'
    )

    request_message = models.TextField(
        blank=True,
        null=True,
        verbose_name='پیام درخواست'
    )

    response_message = models.TextField(
        blank=True,
        null=True,
        verbose_name='پاسخ آژانس'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='تاریخ ایجاد'
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='تاریخ آخرین ویرایش'
    )

    isActive = models.BooleanField(
        default=True,
        verbose_name='فعال'
    )

    class Meta:
        db_table = 'agency_collaboration_requests'

        unique_together = ['agency', 'user']
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['agency', 'user']),
            models.Index(fields=['status']),
            models.Index(fields=['isActive']),
        ]

    def __str__(self):
        return f'درخواست {self.user.get_full_name()} برای آژانس {self.agency.name}'

    def clean(self):
        super().clean()

        if self.agency.user == self.user:
            raise ValidationError("کاربر نمی‌تواند با آژانس خود درخواست همکاری دهد")

        if RequestCollaborationAgency.objects.filter(
            agency=self.agency,
            user=self.user
        ).exclude(pk=self.pk).exists():
            raise ValidationError("درخواست برای این کاربر و آژانس قبلاً ثبت شده است")


    def accept(self, response_message=None):
        """
        تایید درخواست همکاری
        """
        self.status = StatusResponse.ACCEPTED
        self.isActive = True
        if response_message:
            self.response_message = response_message
        self.save()

    def reject(self, response_message=None):
        """
        رد درخواست همکاری
        """
        self.status = StatusResponse.REJECTED
        self.isActive = False
        if response_message:
            self.response_message = response_message
        self.save()

    def cancel(self, response_message=None):
        """
        لغو درخواست همکاری
        """
        self.status = StatusResponse.CANCELLED
        self.isActive = False
        if response_message:
            self.response_message = response_message
        self.save()

    @property
    def is_pending(self):
        return self.status == StatusResponse.PENDING

    @property
    def is_accepted(self):
        return self.status == StatusResponse.ACCEPTED and self.isActive

    @property
    def is_rejected(self):
        return self.status == StatusResponse.REJECTED

    @property
    def is_cancelled(self):
        return self.status == StatusResponse.CANCELLED

    def get_status_display(self):
        return dict(StatusResponse.choices).get(self.status, self.status)


