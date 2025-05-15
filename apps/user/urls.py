from django.urls import path
from .views.user_view import RegisterOrLoginUserAPIView

urlpatterns = [

   path('login',RegisterOrLoginUserAPIView.as_view())

]
