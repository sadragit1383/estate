from django.contrib import admin
from .models.location_model import Country, Province, City, Area

class ProvinceInline(admin.TabularInline):
    model = Province
    extra = 1
    fields = ('name', 'slug')
    # حذف readonly_fields چون created_at وجود ندارد

class CityInline(admin.TabularInline):
    model = City
    extra = 1
    fields = ('name', 'slug', 'province')
    # حذف readonly_fields چون created_at وجود ندارد

class AreaInline(admin.TabularInline):
    model = Area
    extra = 1
    fields = ('name', 'slug', 'city')
    # حذف readonly_fields چون created_at وجود ندارد

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'province_count')
    list_filter = ()  # حذف فیلتر created_at
    search_fields = ('name', 'slug')
    inlines = [ProvinceInline]
    fields = ('name', 'slug')  # فقط فیلدهای موجود

    def province_count(self, obj):
        return obj.provinces.count()
    province_count.short_description = 'تعداد استان‌ها'

@admin.register(Province)
class ProvinceAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'slug', 'city_count')
    list_filter = ('country',)  # حذف created_at
    search_fields = ('name', 'slug', 'country__name')
    inlines = [CityInline]
    autocomplete_fields = ['country']
    fields = ('name', 'slug', 'country')  # فقط فیلدهای موجود

    def city_count(self, obj):
        return obj.cities.count()
    city_count.short_description = 'تعداد شهرها'

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'province', 'country', 'slug', 'area_count')
    list_filter = ('province__country', 'province')  # حذف created_at
    search_fields = ('name', 'slug', 'province__name')
    inlines = [AreaInline]
    autocomplete_fields = ['province']
    fields = ('name', 'slug', 'province')  # فقط فیلدهای موجود

    def country(self, obj):
        return obj.province.country
    country.short_description = 'کشور'

    def area_count(self, obj):
        return obj.neighborhoods.count()
    area_count.short_description = 'تعداد محله‌ها'

@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'province', 'country', 'slug')
    list_filter = ('city__province__country', 'city__province', 'city')  # حذف created_at
    search_fields = ('name', 'slug', 'city__name')
    autocomplete_fields = ['city']
    fields = ('name', 'slug', 'city')  # فقط فیلدهای موجود

    def province(self, obj):
        return obj.city.province
    province.short_description = 'استان'

    def country(self, obj):
        return obj.city.province.country
    country.short_description = 'کشور'