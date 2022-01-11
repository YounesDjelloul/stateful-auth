from django.urls import path
from .views import *

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('access_token/refresh/', RefreshAccessTokenView.as_view(), name='refresh_access_token'),
    path('password/reset/', ResetPasswordView.as_view(), name='reset_password'),
]