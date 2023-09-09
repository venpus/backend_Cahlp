from rest_framework.permissions import AllowAny
from backend.models.usermodel import Account
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login
from backend.serializers.usersserializers import UserRegistrationSerializer, UserLoginSerializer

class UserRegistrationAPIView(APIView):
    permission_classes = (AllowAny,)
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "message": "User registered successfully."}, status=status.HTTP_201_CREATED)
        else:
            return Response({"status": "fail", "message": serializer.errors},  status=status.HTTP_406_NOT_ACCEPTABLE)

class UserLoginAPIView(APIView):
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
                return Response({"status": "success",'token': token.key}, status=status.HTTP_200_OK)
            else:
                return Response({'status' : "fail",'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
