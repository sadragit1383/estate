from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models.agency_model import Agency, Consultant, Manager

class CityInline(admin.TabularInline):
    model = Agency.cities.through
    extra = 1
    verbose_name = _("City")
    verbose_name_plural = _("Cities")

class AgencyAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'status', 'province', 'created_at')
    list_filter = ('status', 'province', 'created_at')
    search_fields = ('name', 'user__username', 'user__phone')
    readonly_fields = ('created_at', 'updated_at')
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
            'fields': ('created_at', 'updated_at'),
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
    list_display = ('user', 'agency', 'created_at')
    search_fields = ('user__username', 'user__phone', 'agency__name')
    readonly_fields = ('created_at', 'updated_at')
    list_filter = ('agency', 'created_at')

@admin.register(Consultant)
class ConsultantAdmin(StaffAdmin):
    pass

@admin.register(Manager)
class ManagerAdmin(StaffAdmin):
    pass

admin.site.register(Agency, AgencyAdmin)