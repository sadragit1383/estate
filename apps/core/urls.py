from django.urls import path
from .views.location_view import CountryListView, ProvinceListView, CityListView, AreaListView

urlpatterns = [
    path('countries', CountryListView.as_view()),
    path('countries/<uuid:countryId>/provinces', ProvinceListView.as_view()),
    path('provinces/<uuid:provinceId>/cities', CityListView.as_view()),
    path('cities/<uuid:cityId>/areas', AreaListView.as_view()),
]
