from django.urls import path
from .views.adv import AdvertisementListView

urlpatterns = [

    path('advertisements', AdvertisementListView.as_view()),

]
