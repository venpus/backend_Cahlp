from rest_framework import serializers

from django.contrib.auth import get_user_model
User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    """_summary_
    serializer for user register 
    Args:
        serializers (_type_): _description_

    Returns:
        _type_: _description_
    """
    status = serializers.CharField(write_only=True, default='success', required=False)

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'mobile', 'status')
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        status = validated_data.pop('status', 'success')
        try:
            user = User.objects.create_user(
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
    """_summary_
    serializer for user login
    Args:
        serializers (_type_): _description_
    """
    username = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    password = serializers.CharField(style={'input_type': 'password'})