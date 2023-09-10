from rest_framework import serializers
from backend.models.devicemodel import Device, DeviceData
from django.contrib.auth import get_user_model
User = get_user_model()


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ['mac', 'user']

class DeviceDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceData
        exclude = ['date_joined']