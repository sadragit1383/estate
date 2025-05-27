from django.urls import path
from .views.agency_view import AgencyCreateAPIView

urlpatterns = [

    path('create/agency', AgencyCreateAPIView.as_view())

]
