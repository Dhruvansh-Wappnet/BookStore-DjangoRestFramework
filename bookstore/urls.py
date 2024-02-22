# urls.py
from django.urls import path
from .views import AddBookAPIView, BookAPIView, UserRegistrationAPIView, UserLoginAPIView, ForgetPasswordAPIView, VerifyOTPAPIView, ResetPasswordAPIView
from rest_framework.authtoken.views import ObtainAuthToken

urlpatterns = [
    path('register/', UserRegistrationAPIView.as_view(), name='user-registration'),
    path('add-book/', AddBookAPIView.as_view(), name='add-book'),
    path('booking/', BookAPIView.as_view(), name='booking'),
    path('login/', UserLoginAPIView.as_view(), name='login'),
    path('forget_password/', ForgetPasswordAPIView.as_view(), name='forget-password'),
    path('verify_otp/', VerifyOTPAPIView.as_view(), name='verify-otp'),
    path('reset_password/', ResetPasswordAPIView.as_view(), name='reset-password'),
    # path('login/', ObtainAuthToken.as_view(), name='login'),
]
