from rest_framework import serializers
from backend.models.devicemodel import Device, DeviceData
from datetime import datetime
from django.contrib.auth import get_user_model
User = get_user_model()


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ['mac', 'user']

class DeviceDataSerializer(serializers.ModelSerializer):
    ph = serializers.IntegerField(source='PH_sensor_data')
    temp = serializers.IntegerField(source='T_sensor_data')
    tds = serializers.IntegerField(source='TDS_sensor_data')
    created_at = serializers.DateTimeField(format="%Y%m%d%H%M%S")
    class Meta:
        model = DeviceData
        fields = ("ph", "temp", "tds", "created_at")
        
class DeviceDataValidationSerializer(serializers.Serializer):
    ph = serializers.IntegerField()
    temp = serializers.IntegerField()
    tds = serializers.IntegerField()
    mac = serializers.CharField(max_length=17)
    username = serializers.CharField(max_length=20)

class LatestDeviceDataSerializer(serializers.Serializer):
    ph = serializers.DecimalField(max_digits=5, decimal_places=2, read_only=True)
    temp = serializers.DecimalField(max_digits=5, decimal_places=2, read_only=True)
    tds = serializers.DecimalField(max_digits=5, decimal_places=2, read_only=True)
    mac = serializers.CharField(max_length=17, read_only=True)
    created_at = serializers.DateTimeField(format="%Y%m%d%H%M%S", read_only=True)
    
    def get_latest_data(self, obj):
        # Get the latest DeviceData instance associated with the Device
        latest_data = DeviceData.objects.filter(device=obj).order_by('-created_at').first()
        if latest_data:
            return {
                'ph': latest_data.PH_sensor_data,
                'temp': latest_data.T_sensor_data,
                'tds': latest_data.TDS_sensor_data,
                'mac': latest_data.device.mac,
                'username' : latest_data.device.user.get_username(),
                'created_at': latest_data.created_at.strftime("%Y%m%d%H%M%S")
            }
        return None