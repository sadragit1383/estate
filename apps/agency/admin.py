from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models.agency_model import Agency, Consultant, Manager,RejectedAgency
from .models.requestagency_model import RequestCollaborationAgency,StatusResponse, Role
from django.utils.html import format_html



class CityInline(admin.TabularInline):
    model = Agency.cities.through
    extra = 1
    verbose_name = _("City")
    verbose_name_plural = _("Cities")

class AgencyAdmin(admin.ModelAdmin):

    list_display = ('user_id','name', 'user', 'status', 'province', 'createdAt')
    list_filter = ('status', 'province', 'createdAt')
    search_fields = ('name', 'user__username', 'user__phone')
    readonly_fields = ('createdAt', 'updatedAt')
    fieldsets = (
        (_("Basic Information"), {
            'fields': ('user', 'name', 'status')
        }),
        (_("Contact Information"), {
            'fields': ('email', 'address', 'province')
        }),
        (_("Media Files"), {
            'fields': ('profileImage', 'bannerImage', 'logoImage', 'licenceImage'),
            'classes': ('collapse',)
        }),
        (_("Additional Information"), {
            'fields': ('bio', 'timeWork'),
            'classes': ('collapse',)
        }),
        (_("Timestamps"), {
            'fields': ('createdAt', 'updatedAt'),
            'classes': ('collapse',)
        }),
    )
    inlines = [CityInline]
    actions = ['activate_agencies', 'deactivate_agencies', 'reject_agencies']

    def activate_agencies(self, request, queryset):
        queryset.update(status=Agency.Status.ACTIVE)
    activate_agencies.short_description = _("Activate selected agencies")

    def deactivate_agencies(self, request, queryset):
        queryset.update(status=Agency.Status.INACTIVE)
    deactivate_agencies.short_description = _("Deactivate selected agencies")

    def reject_agencies(self, request, queryset):
        for agency in queryset:
            agency.reject_agency(_("Rejected by admin"))
    reject_agencies.short_description = _("Reject selected agencies")

class StaffAdmin(admin.ModelAdmin):
    list_display = ('user', 'agency', 'createdAt')
    search_fields = ('user__username', 'user__phone', 'agency__name')
    readonly_fields = ('createdAt', 'updatedAt')
    list_filter = ('agency', 'createdAt')

@admin.register(Consultant)
class ConsultantAdmin(StaffAdmin):
    pass

@admin.register(Manager)
class ManagerAdmin(StaffAdmin):
    pass

admin.site.register(Agency, AgencyAdmin)



@admin.register(RequestCollaborationAgency)
class RequestCollaborationAgencyAdmin(admin.ModelAdmin):
    list_display = (
        'user_full_name',
        'agency_name',
        'role',
        'status_colored',
        'isActive',
        'createdAt',
    )
    list_filter = ('status', 'role', 'isActive', 'createdAt')
    search_fields = ('user__first_name', 'user__last_name', 'agency__name', 'request_message')
    # readonly_fields = ('createdAt', 'updatedAt')
    ordering = ('-createdAt',)
    list_per_page = 25

    def user_full_name(self, obj):
        return obj.user.get_full_name()
    user_full_name.short_description = 'نام کاربر'

    def agency_name(self, obj):
        return obj.agency.name
    agency_name.short_description = 'نام آژانس'

    def status_colored(self, obj):
        color_map = {
            StatusResponse.PENDING: 'orange',
            StatusResponse.ACCEPTED: 'green',
            StatusResponse.REJECTED: 'red',
            StatusResponse.CANCELLED: 'gray',
        }
        color = color_map.get(obj.status, 'black')
        return format_html('<span style="color: {};">{}</span>', color, obj.get_status_display())
    status_colored.short_description = 'وضعیت'

    fieldsets = (
        (None, {
            'fields': (
                'agency',
                'user',
                'role',
                'status',
                'isActive',
            )
        }),
        ('پیام‌ها', {
            'fields': (
                'request_message',
                'responseMessage',
            )
        }),
        ('تاریخ‌ها', {
            'fields': (
                'createdAt',
                'updatedAt',
            )
        }),
    )


@admin.register(RejectedAgency)
class RejectedAgencyAdmin(admin.ModelAdmin):
    # تنظیمات نمایش لیست رکوردها
    list_display = ('agency_name', 'text', 'createdAt', 'updatedAt')
    list_filter = ('createdAt', 'updatedAt')
    search_fields = ('agency__name', 'text')
    ordering = ('-createdAt',)
    date_hierarchy = 'createdAt'

    # تنظیمات نمایش جزئیات هر رکورد
    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': ('agency', 'text')
        }),
        ('تاریخ‌ها', {
            'fields': ('createdAt', 'updatedAt'),
            'classes': ('collapse',)
        }),
    )

    readonly_fields = ('createdAt', 'updatedAt')

    # تابع سفارشی برای نمایش نام آژانس
    def agency_name(self, obj):
        return obj.agency.name if obj.agency else '-'
    agency_name.short_description = 'نام آژانس'
