from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login
from backend.serializers.usersserializers import UserRegistrationSerializer, UserLoginSerializer
from backend.serializers.deviceserializers import DeviceSerializer
from backend.utility import validate_mac_address
from django.contrib.auth import get_user_model
from django.conf import settings
User = get_user_model()


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
            username : str= serializer.validated_data.get('username')
            email : str = serializer.validated_data.get('email')
            password : str = serializer.validated_data.get('password')
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
        if not validate_mac_address(mac_address):
            return Response({'status' : 'fail','detail': 'Invalid MAC address format'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'MAC Address': mac_address}, status=status.HTTP_200_OK)
    

class SensorDataReceiverView(APIView):
    permission_classes = (IsAuthenticated,)
    
    
class SensorDataRequesterView(APIView):
    permission_classes = (IsAuthenticated,)
    
class DeviceResetView(APIView):
    permission_classes = (IsAuthenticated,)
    
class OTAView(APIView):
    permission_classes = (IsAuthenticated,)