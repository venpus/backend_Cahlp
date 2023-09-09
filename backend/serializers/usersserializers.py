from rest_framework import serializers
from backend.models.usermodel import Account

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('username', 'password', 'email', 'mobile')
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        user = Account.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email'],
            mobile=validated_data['mobile']
        )
        return user