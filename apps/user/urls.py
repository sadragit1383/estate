from django.urls import path
from .views.register_view import RegisterOrLoginUserAPIView

urlpatterns = [

   path('login',RegisterOrLoginUserAPIView.as_view())

]
