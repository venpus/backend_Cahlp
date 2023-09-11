from django.urls import path, re_path
from backend.views import UserRegistrationAPIView, UserLoginAPIView,\
    DeviceRegisterAPIView, MacAddressView, SensorDataReceiverView, \
        SensorDataRequesterView, DeviceResetView, OTAView, NotFoundAPIView

urlpatterns = [
    path('register/', UserRegistrationAPIView.as_view(), name='user-registration'),
    path('login/', UserLoginAPIView.as_view(), name='user-login'),
    path('devreg/', DeviceRegisterAPIView.as_view(), name = "device-register"),
    path('sensors/request/', SensorDataRequesterView.as_view(), name = 'sensor-request'),
    path('sensors/', SensorDataReceiverView.as_view(), name = "sensor-receive"),
    path('devicereset/', DeviceResetView.as_view(), name = 'device-reset'),
    path('ota/', OTAView.as_view(), name = "ota"),
    path('ota/<str:otaquery>', OTAView.as_view(), name = "ota"),
    re_path(r'^(?P<mac_address>([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2}))$', MacAddressView.as_view(), name='mac-address'),
    path('<str:args>', NotFoundAPIView.as_view(), name='not-found-api'),


    
]