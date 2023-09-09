from rest_framework import generics
from rest_framework.permissions import AllowAny
from backend.models.usermodel import Account
from backend.serializers.usersserializers import UserRegistrationSerializer

class UserRegistrationView(generics.CreateAPIView):
    queryset = Account.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = (AllowAny,)