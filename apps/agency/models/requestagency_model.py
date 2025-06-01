from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
import uuid
from apps.user.models.user_model import User
from .agency_model import Agency
from apps.user.models.validation.user_validation import CleanFieldsMixin
from .agency_model import Consultant,Manager,TimestampedModel

class Role(models.TextChoices):
    MANAGER = 'manager', 'مدیر'
    CONSULTANT = 'consultant', 'مشاور'
    ADMIN = 'admin', 'ادمین'


class StatusResponse(models.TextChoices):
    PENDING = 'pending', 'در انتظار بررسی'
    ACCEPTED = 'accepted', 'تایید شده'
    REJECTED = 'rejected', 'رد شده'
    CANCELLED = 'cancelled', 'لغو شده'


class RequestCollaborationAgency(CleanFieldsMixin,TimestampedModel,models.Model):

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

    responseMessage = models.TextField(
        blank=True,
        null=True,
        verbose_name='پاسخ آژانس'
    )



    isActive = models.BooleanField(
        default=True,
        verbose_name='فعال'
    )

    class Meta:
        db_table = 'agency_collaboration_requests'
        ordering = ['-createdAt']
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

        existing_request = RequestCollaborationAgency.objects.filter(
            agency=self.agency,
            user=self.user
        ).exclude(pk=self.pk).order_by('-createdAt').first()

        if existing_request and existing_request.status in ['accepted', 'rejected','pending']:
            raise ValidationError("درخواست برای این کاربر و آژانس قبلاً ثبت و بررسی شده است")



    def accept(self, responseMessage=None):

        from ..models.requestagency_model import Role, StatusResponse

        self.status = StatusResponse.ACCEPTED
        self.isActive = True
        if responseMessage:
            self.responseMessage = responseMessage

        Manager.objects.filter(user=self.user, agency=self.agency).delete()
        Consultant.objects.filter(user=self.user, agency=self.agency).delete()

        # ثبت کاربر در نقش جدید
        if self.role == Role.MANAGER:
            Manager.objects.create(
                user=self.user,
                agency=self.agency,
                isActive=True
            )
        elif self.role == Role.CONSULTANT:
            Consultant.objects.create(
                user=self.user,
                agency=self.agency,
                isActive=True
            )

        self.save()


    def reject(self, responseMessage=None):
        """
        رد درخواست همکاری
        """
        self.status = StatusResponse.REJECTED
        self.isActive = False
        if responseMessage:
            self.responseMessage = responseMessage
        self.save()


    def cancel(self, responseMessage=None):
        """
        لغو درخواست همکاری
        """
        self.status = StatusResponse.CANCELLED
        self.isActive = False
        if responseMessage:
            self.responseMessage = responseMessage
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


