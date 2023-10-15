from django.urls import path, re_path
from backend.views import UserRegistrationAPIView, UserLoginAPIView,\
    DeviceRegisterAPIView, MacAddressView, SensorDataReceiverView, \
        SensorDataRequesterView, DeviceResetView, OTAView, CAMView, CAMSettingView, NotFoundAPIView, UserNameDuplicateCheckerView, \
        ResetUserPasswordView, SearchDataView, WithdrawalView, SetdevstatView, DevstatchkView

urlpatterns = [
    path('register/', UserRegistrationAPIView.as_view(), name='user-registration'),
    path('login/', UserLoginAPIView.as_view(), name='user-login'),
    path('devreg/', DeviceRegisterAPIView.as_view(), name = "device-register"),
    path('sensors/request/', SensorDataRequesterView.as_view(), name = 'sensor-request'),
    path('sensors/', SensorDataReceiverView.as_view(), name = "sensor-receive"),
    path('devicereset/', DeviceResetView.as_view(), name = 'device-reset'),
    path('ota/', OTAView.as_view(), name = "ota"),
    path('ota/<str:otaquery>', OTAView.as_view(), name = "ota"),
    path('cam/', CAMView.as_view(), name = 'CAM-View'),
    path('cam/setting/', CAMSettingView.as_view(), name = 'CAM-setting'),
    # path('<str:mac_address>', MacAddressView.as_view(), name='mac-address'),
    #path("",NotFoundAPIView.as_view(), name = "not-found")
    #new update 2023 - 10 -10
    path('checkduplicate/', UserNameDuplicateCheckerView.as_view(), name='duplicate-username-check'),
    path('resetpass/', ResetUserPasswordView.as_view(), name='reset-password'),
    path('searchdata/', SearchDataView.as_view(), name='search-data'),
    path('withdrawal/', WithdrawalView.as_view(), name='withdrawal'),
    path("devstatchk/", DevstatchkView.as_view(), name = "devstatchk"),
    path('setdevstat/', SetdevstatView.as_view(), name='setdevstat'),


    
]