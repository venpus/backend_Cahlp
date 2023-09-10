from django.urls import path
from backend.views import UserRegistrationAPIView, UserLoginAPIView, DeviceRegisterAPIView

urlpatterns = [
    path('register/', UserRegistrationAPIView.as_view(), name='user-registration'),
    path('login/', UserLoginAPIView.as_view(), name='user-login'),
    path('devreg/', DeviceRegisterAPIView.as_view(), name = "device-register")
]