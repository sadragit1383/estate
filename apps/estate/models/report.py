from django.db import models
from django.utils.translation import gettext_lazy as _
from .base import BaseModel

class ReportType(BaseModel):
    name = models.CharField(max_length=100, verbose_name=_('نام نوع گزارش'))

    class Meta:
        verbose_name = _('نوع گزارش')
        verbose_name_plural = _('انواع گزارش‌ها')

class Report(BaseModel):
    class ReportGrade(models.TextChoices):
        NORMAL = 'normal', _('عادی')
        MEDIUM = 'medium', _('متوسط')
        URGENT = 'urgent', _('فوری')

    class ReportStatus(models.TextChoices):
        PENDING = 'pending', _('در انتظار')
        IN_PROGRESS = 'in_progress', _('در حال بررسی')
        RESOLVED = 'resolved', _('حل شده')

    report_type = models.ForeignKey(
        ReportType,
        on_delete=models.PROTECT,
        verbose_name=_('نوع گزارش')
    )

    grade = models.CharField(
        max_length=20,
        choices=ReportGrade.choices,
        default=ReportGrade.NORMAL,
        verbose_name=_('سطح اهمیت')
    )

    status = models.CharField(
        max_length=20,
        choices=ReportStatus.choices,
        default=ReportStatus.PENDING,
        verbose_name=_('وضعیت')
    )

    description = models.TextField(verbose_name=_('توضیحات'))
    error_time = models.DateTimeField(
        verbose_name=_('زمان خطا'),
        null=True,
        blank=True
    )

    is_handled = models.BooleanField(
        default=False,
        verbose_name=_('بررسی شده')
    )

    class Meta:
        verbose_name = _('گزارش')
        verbose_name_plural = _('گزارش‌ها')
