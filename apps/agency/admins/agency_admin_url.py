from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .agency_admin import AgencyAdminViewSet, ConsultantAdminViewSet, ManagerAdminViewSet, RejectedAgencyAdminViewSet

router = DefaultRouter()
router.register(r'agencies', AgencyAdminViewSet, basename='agency-admin')
router.register(r'consultants', ConsultantAdminViewSet, basename='consultant-admin')
router.register(r'managers', ManagerAdminViewSet, basename='manager-admin')
router.register(r'rejectedagencies', RejectedAgencyAdminViewSet, basename='rejected-agency-admin')

urlpatterns = [
    path('api/admin', include(router.urls)),
]