from rest_framework import serializers
from backend.models.devicemodel import Device

class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ['mac', 'user']