from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

class Device(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mac = models.CharField(max_length=17, unique=True)  # MAC address is typically 17 characters long (e.g., "00:1A:2B:3C:4D:5E")
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    def __str__(self):
        return self.mac

class DeviceData(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    PH_sensor_data = models.CharField(max_length=17, unique=True, default='', null=True)
    T_sensor_data = models.CharField(max_length=17, unique=True, default='', null=True)
    TDS_sensor_data = models.CharField(max_length=17, unique=True, default='', null=True)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    def __str__(self):
        return "mac: {}, ph: {}, temp: {}, tds: {}".format(Device.mac, self.PH_sensor_data, self.T_sensor_data, self.TDS_sensor_data)