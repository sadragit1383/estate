from django.contrib import admin
from .models.advertisement import *
from .models.feature import Feature, FeatureValue, TypeFeature
from .models.feature import AdvertisementFeature
from .models.gallery import AdvertisementGallery


@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    search_fields = ['title']


@admin.register(FeatureValue)
class FeatureValueAdmin(admin.ModelAdmin):
    search_fields = ['title']


@admin.register(TypeFeature)
class TypeFeatureAdmin(admin.ModelAdmin):
    search_fields = ['title']


class AdvertisementFeatureInline(admin.TabularInline):
    model = AdvertisementFeature
    extra = 1
    autocomplete_fields = ['feature', 'value']


class AdvertisementGalleryInline(admin.TabularInline):
    model = AdvertisementGallery
    extra = 1
    readonly_fields = ['thumbnail_preview']
    fields = ['org_image', 'thumbnail_preview']
    # برای نمایش عکس بندانگشتی داخل پنل (غیر قابل ویرایش)
    def thumbnail_preview(self, obj):
        if obj.thumbnail:
            return f'<img src="{obj.thumbnail.url}" style="width: 120px; height: auto;" />'
        return "-"
    thumbnail_preview.allow_tags = True
    thumbnail_preview.short_description = "پیش‌نمایش"


@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'advType', 'propertyType', 'status', 'expired_at', 'is_expired']
    list_filter = ['advType', 'propertyType', 'status']
    search_fields = ['title', 'description']
    autocomplete_fields = ['user', 'userConfirm']
    inlines = [AdvertisementFeatureInline, AdvertisementGalleryInline]
    readonly_fields = ['viewCount', 'is_expired']
    fieldsets = (
        (None, {
            'fields': ('title', 'user', 'userConfirm', 'advType', 'propertyType', 'status', 'premiumtypes')
        }),
        ('توضیحات', {
            'fields': ('description','price')
        }),
        ('اطلاعات سیستم', {
            'fields': ('viewCount', 'expired_at', 'is_expired')
        }),
    )


@admin.register(AdvertisementFeature)
class AdvertisementFeatureAdmin(admin.ModelAdmin):
    list_display = ['advertisement', 'feature', 'value']
    list_filter = ['feature']
    autocomplete_fields = ['advertisement', 'feature', 'value']



@admin.register(AdvertisementType)
class AdvertisementTypeAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug']
    search_fields = ['title', 'slug']
    prepopulated_fields = {'slug': ('title',)}  # اگر فیلد slug دارید


@admin.register(PropertyType)
class PropertyTypeAdmin(admin.ModelAdmin):
    list_display = ['title', 'parent']
    search_fields = ['title', 'slug']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ['advertisement_types']  # انتخاب راحت‌تر M2M
    list_filter = ['parent']

    # برای نمایش درختی ساده، می‌توانیم یک متد اضافه کنیم (اختیاری)
    def children_count(self, obj):
        return obj.children.count()
    children_count.short_description = 'تعداد زیرمجموعه‌ها'


@admin.register(StatusAdvertisemen)
class StatusAdvertisemenAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug']
    search_fields = ['title', 'slug']
    prepopulated_fields = {'slug': ('title',)}


@admin.register(TypePremium)
class TypePremiumAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug']
    search_fields = ['title', 'slug']
    prepopulated_fields = {'slug': ('title',)}