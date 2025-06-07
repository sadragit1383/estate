from django.db import models
from django.utils import timezone
import uuid

class BaseModel(models.Model):
    """
    مدل پایه که شامل فیلدهای مشترک بین تمام مدل‌ها می‌شود
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    createdAt = models.DateTimeField(default=timezone.now, verbose_name='تاریخ ایجاد')
    updatedAt = models.DateTimeField(auto_now=True, verbose_name='آخرین به‌روزرسانی')
    isActive = models.BooleanField(default=True, verbose_name='فعال')

    class Meta:
        abstract = True


class SlugBaseModel(BaseModel):
    """
    مدل پایه برای مدل‌هایی که نیاز به فیلد slug دارند
    """
    title = models.CharField(max_length=100, verbose_name='عنوان')
    slug = models.SlugField(max_length=100, verbose_name='اسلاگ', unique=True, blank=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_slug()
        super().save(*args, **kwargs)

    def generate_slug(self):
        # پیاده‌سازی منطق تولید slug
        from django.utils.text import slugify
        return slugify(self.title)