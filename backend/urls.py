from django.urls import path
from backend.views import UserRegistrationAPIView, UserLoginAPIView,\
    DeviceRegisterAPIView, MacAddressView, SensorDataReceiverView, \
        SensorDataRequesterView, DeviceResetView, OTAView

urlpatterns = [
    path('register/', UserRegistrationAPIView.as_view(), name='user-registration'),
    path('login/', UserLoginAPIView.as_view(), name='user-login'),
    path('devreg/', DeviceRegisterAPIView.as_view(), name = "device-register"),
    path('<str:mac_address>/', MacAddressView.as_view(), name = "mac-address"),
    path('sensors/request/', SensorDataRequesterView.as_view(), name = 'sensor-request'),
    path('sensors/', SensorDataReceiverView.as_view(), name = "sensor-receive"),
    path('devicereset/', DeviceResetView.as_view(), name = 'device-reset'),
    path('ota/', OTAView.as_view(), name = "ota")

    
]