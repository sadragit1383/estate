from django.db import models

class FeatureGroup(models.TextChoices):
    ADDITIONAL = "additionalFilters", "ویژگی اضافی"
    AMENITIES = "amenities", "امکانات"
    MAIN = "mainFeature", "ویژگی اصلی"

class FeatureValueType(models.TextChoices):
    NUMBER = "number", "عدد"
    STRING = "string", "رشته"
    BOOLEAN = "bool", "منطقی"

class ReportType(models.TextChoices):
    SUPPORT = "support", "پشتیبانی"
    ERROR = "error", "گزارش خطا"

class ReportGrade(models.TextChoices):
    NORMAL = "normal", "عادی"
    MEDIUM = "medium", "متوسط"
    URGENT = "urgent", "فوری"