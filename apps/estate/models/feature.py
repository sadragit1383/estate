# apps/estate/models/feature.py

from django.db import models
from .base import SlugBaseModel
from .enums import FeatureGroup, FeatureValueType


class TypeFeature(SlugBaseModel):
    class Meta:
        verbose_name = 'نوع ویژگی'
        verbose_name_plural = 'انواع ویژگی‌ها'


class Feature(SlugBaseModel):
    typeFeature = models.ForeignKey(TypeFeature, on_delete=models.CASCADE, related_name='features', verbose_name='نوع ویژگی')
    propertyTypes = models.ManyToManyField('estate.PropertyType', related_name="features", verbose_name="نوع ملک")
    typeGroup = models.CharField(max_length=50, choices=FeatureGroup.choices, verbose_name='نوع دسته‌بندی')
    typeValue = models.CharField(max_length=50, choices=FeatureValueType.choices, verbose_name='نوع داده')

    class Meta:
        verbose_name = 'ویژگی'
        verbose_name_plural = 'ویژگی‌ها'


class FeatureValue(SlugBaseModel):
    feature = models.ForeignKey(Feature, on_delete=models.CASCADE, related_name='values', verbose_name='ویژگی')

    class Meta:
        verbose_name = 'مقدار ویژگی'
        verbose_name_plural = 'مقادیر ویژگی‌ها'


class AdvertisementFeature(models.Model):
    advertisement = models.ForeignKey('estate.Advertisement', on_delete=models.CASCADE, related_name='ad_features', verbose_name='آگهی')
    feature = models.ForeignKey(Feature, on_delete=models.CASCADE, related_name='feature_ads', verbose_name='ویژگی')
    value = models.ForeignKey(FeatureValue, on_delete=models.CASCADE, null=True, blank=True, verbose_name='مقدار')

    class Meta:
        verbose_name = 'ویژگی آگهی'
        verbose_name_plural = 'ویژگی‌های آگهی'
        unique_together = ('advertisement', 'feature')
