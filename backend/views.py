from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login
from backend.serializers.usersserializers import UserRegistrationSerializer, UserLoginSerializer
from backend.serializers.deviceserializers import DeviceSerializer, DeviceDataSerializer, DeviceDataValidationSerializer,\
    LatestDeviceDataSerializer
from django.contrib.auth import get_user_model
from backend.models.devicemodel import DeviceData, Device, OTAUpdate
from django.conf import settings
User = get_user_model()

class NotFoundAPIView(APIView):
    def get(self, request,args, format=None):
        # Raise an Http404 exception to indicate that the resource was not found
        return Response({"status" : "fail", "detail" : "endpoint not found"}, status=status.HTTP_417_EXPECTATION_FAILED)

class UserRegistrationAPIView(APIView):
    """
    user register view
    """
    permission_classes = (AllowAny,)
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "detail": "User registered successfully."}, status=status.HTTP_201_CREATED)
        else:
            return Response({"status": "fail", "detail": serializer.errors},  status=status.HTTP_406_NOT_ACCEPTABLE)

class UserLoginAPIView(APIView):
    """
    user login view
    """
    permission_classes = (AllowAny,)
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            print(serializer.validated_data)
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
                return Response({"status": "success",'detail': token.key}, status=status.HTTP_200_OK)
            else:
                return Response({'status' : "fail",'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)


class DeviceRegisterAPIView(APIView):
    """
    device register view
    """
    permission_classes = (IsAuthenticated,)
    def get(self, request, format=None):
        mac_param = request.query_params.get('mac', None)
        username_param = request.query_params.get('username', None)
        if mac_param is None or username_param is None:
            return Response({"status": "fail", "detail": "Both 'mac' and 'username' parameters are required."}, status=status.HTTP_400_BAD_REQUEST)
        # Check if the user with the provided username exists
        try:
            user = User.objects.get(username=username_param)
        except User.DoesNotExist:
            return Response({"status": "fail", "detail": "User does not exist."}, status=status.HTTP_404_NOT_FOUND)
        if request.user.username != username_param:
            return Response({"status" : "fail", "detail" : "must login with username before register"}, status= status.HTTP_406_NOT_ACCEPTABLE)
        # Create a new Device instance
        device_data = {'mac': mac_param, 'user': user.id}
        serializer = DeviceSerializer(data=device_data)
        if serializer.is_valid():
            serializer.save()
            stream_link = f"{settings.SITE_NAME}/{mac_param}"
            return Response({"status": "success", "detail" : stream_link}, status=status.HTTP_201_CREATED)
        else:
            return Response({"status" : "fail", "detail" : serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class MacAddressView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, mac_address, format=None):
        device_data = DeviceData.objects.filter(device__mac=mac_address, device__user__username=request.user.username)
        serializer = DeviceDataSerializer(device_data, many=True)
        return Response({"status" : "success", "detail" : serializer.data}, status=status.HTTP_200_OK)
    

class SensorDataReceiverView(APIView):
    permission_classes = (IsAuthenticated,)
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
            # Check if a Device with the provided mac address exists
            try:
                device = Device.objects.get(mac=mac, user__username=request.user.username)
            except Device.DoesNotExist:
                return Response({"status": "fail", "detail": "Device(mac) not found"}, status=status.HTTP_404_NOT_FOUND)
            # Create a DeviceData instance with the parsed data
            device_data = DeviceData(
                device=device,
                PH_sensor_data=ph,
                T_sensor_data=temp,
                TDS_sensor_data=tds
            )
            # Save the data to the DeviceData model
            device_data.save()
            return Response({"status": "success", "detail" : "data saved"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"status" : "fail", "detail" : serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
class SensorDataRequesterView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, format=None):
        mac_address = request.query_params.get('mac', None)
        try:
            # Find the device by MAC address
            device = Device.objects.get(mac=mac_address, user__username=request.user.username)
        except Device.DoesNotExist:
            return Response({"status": "error", "detail": "Device not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = LatestDeviceDataSerializer(device)
        # Serialize the data and return the response
        data = serializer.get_latest_data(device)
        if data:
            return Response({"status" : "success", "detail": data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "detail": "No data available"}, status=status.HTTP_404_NOT_FOUND)
class DeviceResetView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, format=None):
        mac_address = request.query_params.get('mac', None)
        username =  request.query_params.get('username', None)
        try:
            # Find the device by MAC address
            device = Device.objects.get(mac=mac_address, user__username=request.user.username)
        except Device.DoesNotExist:
            return Response({"status": "error", "detail": "Device not found"}, status=status.HTTP_404_NOT_FOUND)
        device_data_to_delete = DeviceData.objects.filter(device=device)
        device_data_to_delete.delete()
        return Response({"status" : "success", "detail" : "all device data deleted"}, status=status.HTTP_200_OK)
class OTAView(APIView):
    permission_classes = (AllowAny,)
    def get(self, request,otaquery = None,  format=None):
        print(otaquery)
        ota_updates = OTAUpdate.objects.all()
        latest_ota_update = None
        for update in ota_updates:
            if latest_ota_update is None or update.created_at > latest_ota_update.created_at:
                latest_ota_update = update
        input_param = request.query_params.get("vcheck", None)
        if input_param != None and input_param == "OTAversion":
            if latest_ota_update:
                # latest_firmware_file = latest_ota_update.firmware_file
                return Response({"status": "success", "detail" : latest_ota_update.version}, status=status.HTTP_200_OK)
            else:
                return Response({"status": "fail", "detail": "No OTA updates available"}, status=status.HTTP_404_NOT_FOUND)
        if otaquery !=None and otaquery.lower() == "update":
            if latest_ota_update:
                latest_firmware_file = latest_ota_update.firmware_file
                return Response({"status": "success", "detail" : {"link" : f"{settings.SITE_NAME}{latest_firmware_file.url}", "version" : latest_ota_update.version}}, status=status.HTTP_200_OK)
            else:
                return Response({"status": "fail", "detail": "No OTA updates available"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"status" : "fail", "detail" : "invalid endpoint"}, status=status.HTTP_204_NO_CONTENT)