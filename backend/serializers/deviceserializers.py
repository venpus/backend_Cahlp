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
        
class DeviceDataValidationSerializer(serializers.Serializer):
    ph = serializers.IntegerField()
    temp = serializers.IntegerField()
    tds = serializers.IntegerField()
    mac = serializers.CharField(max_length=17)

class LatestDeviceDataSerializer(serializers.Serializer):
    ph = serializers.DecimalField(max_digits=5, decimal_places=2, read_only=True)
    temp = serializers.DecimalField(max_digits=5, decimal_places=2, read_only=True)
    tds = serializers.DecimalField(max_digits=5, decimal_places=2, read_only=True)
    mac = serializers.CharField(max_length=17, read_only=True)
    date_joined = serializers.DateTimeField(read_only=True)
    
    def get_latest_data(self, obj):
        # Get the latest DeviceData instance associated with the Device
        latest_data = DeviceData.objects.filter(device=obj).order_by('-date_joined').first()
        if latest_data:
            return {
                'ph': latest_data.PH_sensor_data,
                'temp': latest_data.T_sensor_data,
                'tds': latest_data.TDS_sensor_data,
                #'mac': latest_data.device.mac,
                #'date_joined': latest_data.date_joined
            }
        return None