from django.db import models
from .base import SlugBaseModel
from .enums import *

class TypeFeature(SlugBaseModel):
    class Meta:
        verbose_name = 'نوع ویژگی'
        verbose_name_plural = 'انواع ویژگی‌ها'


class Feature(SlugBaseModel):



    typeFeature = models.ForeignKey(
        TypeFeature,
        on_delete=models.CASCADE,
        verbose_name='نوع ویژگی',
        related_name='features'
    )

    propertyTypes = models.ManyToManyField(
        'PropertyType',
        related_name="features",
        verbose_name="نوع ملک"
    )


    typeGroup = models.CharField(
        max_length=50,
        verbose_name='نوع دسته بندی',
        choices=FeatureGroup.choices
    )

    typeValue = models.CharField(
        max_length=50,
        verbose_name='نوع داده',
        choices = FeatureValueType.choices
    )

    class Meta:
        verbose_name = 'ویژگی'
        verbose_name_plural = 'ویژگی‌ها'



class FeatureValue(SlugBaseModel):

    feature = models.ForeignKey(
        Feature,
        on_delete=models.CASCADE,
        verbose_name='ویژگی',
        related_name='values'
    )

    class Meta:
        verbose_name = 'مقدار ویژگی'
        verbose_name_plural = 'مقادیر ویژگی‌ها'