from django.db import models


class AbstractBaseModel(models.Model):

    createAt = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updateAt = models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')

    class Meta:
        abstract = True