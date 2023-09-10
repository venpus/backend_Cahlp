from backend.models.usermodel import Account
from backend.models.devicemodel import Device, DeviceData
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin

@admin.register(Account)
class CustomUserAdmin(UserAdmin):
    """_summary_
    custom user model that can access by admin panel
    Args:
        UserAdmin (_type_): _description_
    """
    model = Account
    list_display : tuple = ('email', 'username', 'mobile','date_joined', 'last_login', 'is_admin', 'is_staff')
    search_fields : tuple = ('email', 'username',)
    readonly_fields : tuple = ('date_joined', 'last_login',)
    filter_horizontal : tuple= ()
    list_filter : tuple = ()
    fieldsets : tuple = ()

@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('mac', 'user_username')  # Add 'mac' and 'user_username'

    def user_username(self, obj):
        return obj.user.username
    user_username.short_description = 'User Username'  #

@admin.register(DeviceData)
class DeviceDataAdmin(admin.ModelAdmin):
    list_display = ("user_username", "device_mac", "PH_sensor_data", "T_sensor_data", "TDS_sensor_data", "date_joined")
    def device_mac(self, obj):
        return obj.device.mac
    def user_username(self, obj):
        return obj.device.user.username
    device_mac.short_description = "mac address"
    user_username.short_description = 'User Username'  #