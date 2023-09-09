from rest_framework import serializers
from backend.models.usermodel import Account

class UserRegistrationSerializer(serializers.ModelSerializer):
    status = serializers.CharField(write_only=True, default='success', required=False)

    class Meta:
        model = Account
        fields = ('username', 'password', 'email', 'mobile', 'status')
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        status = validated_data.pop('status', 'success')

        try:
            user = Account.objects.create_user(
                username=validated_data['username'],
                password=validated_data['password'],
                email=validated_data['email'],
                mobile=validated_data['mobile']
            )
        except Exception as e:
            status = 'failed'
            user = None

        return {
            'status': status,
            'user': user
        }



class UserLoginSerializer(serializers.Serializer):
    #username = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    password = serializers.CharField(style={'input_type': 'password'})