from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login
from backend.serializers.usersserializers import UserRegistrationSerializer, UserLoginSerializer
from backend.serializers.deviceserializers import DeviceSerializer, DeviceDataSerializer, DeviceDataValidationSerializer,\
    LatestDeviceDataSerializer
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from backend.models.devicemodel import DeviceData, Device, OTAUpdate
from django.conf import settings
from datetime import datetime
User = get_user_model()

class NotFoundAPIView(APIView):
    def get(self, request,args, format=None):
        # Raise an Http404 exception to indicate that the resource was not found
        return Response({"ret" : "fail", "detail" : "endpoint not found"}, status=status.HTTP_417_EXPECTATION_FAILED)

class UserRegistrationAPIView(APIView):
    """
    user register view
    """
    permission_classes = (AllowAny,)
    def post(self, request):
        username = request.data.get("username","")
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"ret": "success", "detail": "User registered successfully.", "username" : username, "mac" : ""}, status=status.HTTP_201_CREATED)
        else:
            return Response({"ret": "fail", "detail": serializer.errors},  status=status.HTTP_406_NOT_ACCEPTABLE)

class UserLoginAPIView(APIView):
    """
    user login view
    """
    permission_classes = (AllowAny,)
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')
            user = None
            if username:
                user = authenticate(username=username, password=password)
            elif email:
                user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                token, created = Token.objects.get_or_create(user=user)
                return Response({"ret": "success",'detail': "successfullly logged in", "token" :  token.key, "username" : username, "mac" : ""}, status=status.HTTP_200_OK)
            else:
                return Response({'ret' : "fail",'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)


class DeviceRegisterAPIView(APIView):
    """
    device register view
    """
    permission_classes = (AllowAny,)
    def get(self, request, format=None):
        mac_param = request.query_params.get('mac', None)
        username_param = request.query_params.get('username', None)
        if mac_param is None or username_param is None:
            return Response({"ret": "fail", "detail": "Both 'mac' and 'username' parameters are required."}, status=status.HTTP_400_BAD_REQUEST)
        # Check if the user with the provided username exists
        try:
            user = User.objects.get(username=username_param)
        except User.DoesNotExist:
            return Response({"ret": "fail", "detail": "User does not exist."}, status=status.HTTP_404_NOT_FOUND)
        
        # Create a new Device instance
        device_data = {'mac': mac_param, 'user': user.id}
        serializer = DeviceSerializer(data=device_data)
        if serializer.is_valid():
            serializer.save()
            stream_link = f"{settings.STEAM_SITE}t{mac_param.replace(':','').lower()}"
            return Response({"ret": "success", "live" : stream_link, "username" : username_param, "mac" : mac_param}, status=status.HTTP_201_CREATED)
        else:
            return Response({"ret" : "fail", "detail" : serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class MacAddressView(APIView):
    permission_classes = (AllowAny,)
    def get(self, request, mac_address, format=None):
        device_data = DeviceData.objects.filter(device__mac=mac_address)
        serializer = DeviceDataSerializer(device_data, many=True)
        return Response({"ret" : "success", "data" : serializer.data, "mac" : mac_address}, status=status.HTTP_200_OK)
    

class SensorDataReceiverView(APIView):
    permission_classes = (AllowAny,)
    def get(self, request, format=None):
        # Deserialize the request data using the serializer
        serializer = DeviceDataValidationSerializer(data=request.query_params)
        if serializer.is_valid():
            # Extract the deserialized data
            validated_data = serializer.validated_data
            ph = validated_data.get('ph')
            temp = validated_data.get('temp')
            tds = validated_data.get('tds')
            mac = validated_data.get('mac')
            username = validated_data.get('username')
            # Check if a Device with the provided mac address exists
            try:
                device = Device.objects.get(mac=mac, user__username=username)
            except Device.DoesNotExist:
                return Response({"ret": "fail", "detail": "Device(mac) not found"}, status=status.HTTP_404_NOT_FOUND)
            # Create a DeviceData instance with the parsed data
            device_data = DeviceData(
                device=device,
                PH_sensor_data=ph,
                T_sensor_data=temp,
                TDS_sensor_data=tds
            )
            # Save the data to the DeviceData model
            device_data.save()
            return Response({"ret": "success", "detail" : "data saved"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"ret" : "fail", "detail" : serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
class SensorDataRequesterView(APIView):
    permission_classes = (AllowAny,)
    def get(self, request, format=None):
        mac_address = request.query_params.get('mac', None)
        username = request.query_params.get('username', None)
        try:
            # Find the device by MAC address
            device = Device.objects.get(mac=mac_address, user__username=username)
        except Device.DoesNotExist:
            return Response({"ret": "error", "detail": "Device not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = LatestDeviceDataSerializer(device)
        # Serialize the data and return the response
        data = serializer.get_latest_data(device)
        if data:
            data['ret'] = 'success'
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response({"ret": "error", "detail": "No data available"}, status=status.HTTP_404_NOT_FOUND)
class DeviceResetView(APIView):
    permission_classes = (AllowAny,)
    def get(self, request, format=None):
        mac_address = request.query_params.get('mac', None)
        username =  request.query_params.get('username', None)
        try:
            # Find the device by MAC address
            device_to_delete = Device.objects.get(mac=mac_address, user__username=username)
        except Device.DoesNotExist:
            return Response({"ret": "error", "detail": "Device not found"}, status=status.HTTP_404_NOT_FOUND)
        device_to_delete.delete()
        return Response({"ret" : "success", "detail" : "all device data deleted"}, status=status.HTTP_200_OK)
class OTAView(APIView):
    permission_classes = (AllowAny,)
    def get(self, request,otaquery = None,  format=None):
        ota_updates = OTAUpdate.objects.all()
        latest_ota_update = None
        for update in ota_updates:
            if latest_ota_update is None or update.created_at > latest_ota_update.created_at:
                latest_ota_update = update
        input_param = request.query_params.get("vcheck", None)
        if input_param != None and input_param == "OTAversion":
            if latest_ota_update:
                # latest_firmware_file = latest_ota_update.firmware_file
                return Response({"ret": "success", "OTAversion" : latest_ota_update.version}, status=status.HTTP_200_OK)
            else:
                return Response({"ret": "fail", "OTAversion": "No OTA updates available"}, status=status.HTTP_404_NOT_FOUND)
        if otaquery !=None and otaquery.lower() == "update":
            if latest_ota_update:
                latest_firmware_file = latest_ota_update.firmware_file
                return Response({"ret": "success","OTA file link" : f"{settings.SITE_NAME}{latest_firmware_file.url}", "OTAversion" : latest_ota_update.version}, status=status.HTTP_200_OK)
            else:
                return Response({"ret": "fail", "detail": "No OTA updates available"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"ret" : "fail", "detail" : "invalid endpoint"}, status=status.HTTP_204_NO_CONTENT)
    
class CAMView(APIView):
    permission_classes = (AllowAny,)
    def get(self, request,  format=None):
        mac_address = request.query_params.get('mac', None)
        username =  request.query_params.get('username', None)
        setting_param = request.query_params.get('setting', None)
        try:
            # Find the device by MAC address
            device = Device.objects.get(mac=mac_address, user__username=username)
        except Device.DoesNotExist:
            return Response({"ret": "error", "detail": "Device not found"}, status=status.HTTP_404_NOT_FOUND)
        if device.is_cam == True:
            flag = "enable"
        else:
            flag = "disable"
        if setting_param !=None  and setting_param.lower() == 'true':
            device.is_cam = True
            flag = "enable"
        if setting_param !=None  and setting_param.lower() == 'false':
            flag = "disable"
            device.is_cam = False
        device.save()
        return Response({"ret" : "success", "cam" : flag})

class CAMSettingView(APIView):
    permission_classes = (AllowAny,)
    def get(self, request,  format=None):
        mac_address = request.query_params.get('mac', None)
        username =  request.query_params.get('username', None)
        try:
            # Find the device by MAC address
            device = Device.objects.get(mac=mac_address, user__username=username)
        except Device.DoesNotExist:
            return Response({"ret": "error", "detail": "Device not found"}, status=status.HTTP_404_NOT_FOUND)
        if device.is_cam == True:
            flag = "enable"
        else:
            flag = "disable"
        return Response({"ret" : "success", "cam" : flag})
    
#new update 2023 - 10 -10

class UserNameDuplicateCheckerView(APIView):
    permission_classes = (AllowAny,)
    def get(self, request,  format=None):
        username = request.query_params.get('username', None)
        if username:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return Response({"ret": "success", "detail": "Username is available"}, status=status.HTTP_200_OK)
            return Response({"ret": "fail", "detail": "Username is already taken"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"ret": "fail", "detail": "Username is required"}, status=status.HTTP_400_BAD_REQUEST)
    

class ResetUserPasswordView(APIView):
    permission_classes = (AllowAny,)
    def get(self, request,  format=None):
        username = request.query_params.get('username', None)
        newpasword = request.query_params.get("newpass")
        confirmpassword = request.query_params.get("confirm")
        if newpasword != confirmpassword:
            return Response({"ret": "fail", "detail": "Passwords do not match"}, status=status.HTTP_400_BAD_REQUEST)
        if username:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return Response({"ret": "fail", "detail": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)
            user.set_password(newpasword)
            user.save()
            return Response({"ret": "success", "detail": "Password reset successful"}, status=status.HTTP_200_OK)
        return Response({"ret": "fail", "detail": "Username is required"}, status=status.HTTP_400_BAD_REQUEST)

class SearchDataView(APIView):
    permission_classes = (AllowAny,)
    def get(self, request,  format=None):
        mac_address = request.query_params.get('mac', None)
        username =  request.query_params.get('username', None)
        starttime = request.query_params.get("starttime", None)
        endtime = request.query_params.get("endtime", None)

        if mac_address == None or username == None or starttime== None or endtime == None:
             return Response({"ret": "error", "detail": "username, mac, starttime and endtime are required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            starttime = datetime.strptime(starttime, "%Y-%m-%dT%H:%M:%S")
            endtime = datetime.strptime(endtime, "%Y-%m-%dT%H:%M:%S")
        except ValueError:
            return Response({"ret": "error", "detail": "Invalid date format (%Y-%m-%dT%H:%M:%S)"}, status=status.HTTP_400_BAD_REQUEST)


        try:
            # Find the device by MAC address
            device = Device.objects.get(mac=mac_address, user__username=username)
        except Device.DoesNotExist:
            return Response({"ret": "error", "detail": "Device not found"}, status=status.HTTP_404_NOT_FOUND)
        device_data = DeviceData.objects.filter(device__mac=mac_address, created_at__range=(starttime, endtime))
        serializer = DeviceDataSerializer(device_data, many=True)
        return Response({"ret" : "success", "data" : serializer.data, "mac" : mac_address}, status=status.HTTP_200_OK)
    
class WithdrawalView(APIView):
    permission_classes = (AllowAny,)
    def get(self, request,  format=None):
        username = request.query_params.get('username', None)
        password = request.query_params.get("password", None)
        if username:
            user = authenticate(username=username, password=password)
            if user is not None:
                return Response({"ret": "success", "detail": "User verified"}, status=status.HTTP_200_OK)
            return Response({"ret": "fail", "detail": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"ret": "fail", "detail": "Username is required"}, status=status.HTTP_400_BAD_REQUEST)
    
class DevstatchkView(APIView):
    permission_classes = (AllowAny,)
    def get(self, request,  format=None):
        mac_address = request.query_params.get('mac', None)
        username =  request.query_params.get('username', None)
        try:
            # Find the device by MAC address
            device = Device.objects.get(mac=mac_address, user__username=username)
        except Device.DoesNotExist:
            return Response({"ret": "error", "detail": "Device not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = DeviceDataSerializer(device)
        return Response({"ret" : "success", "data" : serializer.data}, status=status.HTTP_200_OK)
    
class SetdevstatView(APIView):
    permission_classes = (AllowAny,)
    def get(self, request, format = None):
        pass