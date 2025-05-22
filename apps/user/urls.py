from django.urls import path
from .views.user_view import GetUserAPIView,ProfileUpdateView,RegisterOrLoginUserAPIView,OTPVerifyAPIView,AdminLoginAPIView

urlpatterns = [

   path('login',RegisterOrLoginUserAPIView.as_view()),
   path('otb',OTPVerifyAPIView.as_view()),
   path('loginadmin',AdminLoginAPIView.as_view()),
   path('updateuser',ProfileUpdateView.as_view()),
   path('getuser',GetUserAPIView.as_view()),

]
