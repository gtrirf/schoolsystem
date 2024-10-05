from django.urls import path
from .views import CompleteRegisterView, VerifySmsView, PhoneNumberView, LoginView, LogoutView
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('phone-number/', PhoneNumberView.as_view(), name='phone_number'),
    path('verify-sms/', VerifySmsView.as_view(), name='verify_sms'),
    path('register/', CompleteRegisterView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='signin'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

