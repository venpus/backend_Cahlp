from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

class Device(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_cam = models.BooleanField(default=False)
    mac = models.CharField(max_length=17, unique=True)  # MAC address is typically 17 characters long (e.g., "00:1A:2B:3C:4D:5E")
    created_at = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    def __str__(self):
        return self.mac

class DeviceData(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    PH_sensor_data = models.IntegerField(default='', null=True)
    T_sensor_data = models.IntegerField(default='', null=True)
    TDS_sensor_data = models.IntegerField(default='', null=True)
    created_at = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    def __str__(self):
        return "mac: {}, ph: {}, temp: {}, tds: {}".format(self.device.mac, self.PH_sensor_data, self.T_sensor_data, self.TDS_sensor_data)
    
class OTAUpdate(models.Model):
    version = models.CharField(max_length=100)
    firmware_file = models.FileField(upload_to='ota_updates/')
    created_at = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    def __str__(self):
        return f"OTA Update - Version: {self.version}"
    
class DevStat(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    hw_version = models.CharField(max_length=100)
    fw_version = models.CharField(max_length=100)
    wifi_name = models.CharField(max_length=100)
    wifi_password = models.CharField(max_length=100)
    created_at = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    def __str__(self):
        return f"DevStat - {self.device.mac} - HV Version: {self.hw_version} - FW Version: {self.fw_version} - Wifi Name: {self.wifi_name} - Wifi Password: {self.wifi_password}"
