from django.urls import path
from .views.user_view import RegisterOrLoginUserAPIView,OTPVerifyAPIView

urlpatterns = [

   path('login',RegisterOrLoginUserAPIView.as_view()),
   path('otb',OTPVerifyAPIView.as_view()),

]
