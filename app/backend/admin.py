from backend.models.usermodel import Account
from backend.models.devicemodel import Device, DeviceData, OTAUpdate, DevStat
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'mobile', 'is_admin', 'is_staff', 'is_active', 'is_user')
    search_fields = ('email', 'username')
    list_filter = ('is_admin', 'is_staff', 'is_active', 'is_user')
    fieldsets = (
        (None, {'fields': ('email', 'username', 'mobile', 'password')}),
        ('Permissions', {'fields': ('is_admin', 'is_staff', 'is_active', 'is_user')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'mobile', 'password1', 'password2', 'is_admin', 'is_staff', 'is_active', 'is_user')}
        ),
    )


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('mac', 'user_username')  # Add 'mac' and 'user_username'

    def user_username(self, obj):
        return obj.user.username
    user_username.short_description = 'User Username'  #

@admin.register(DeviceData)
class DeviceDataAdmin(admin.ModelAdmin):
    list_display = ("user_username", "device_mac", "PH_sensor_data", "T_sensor_data", "TDS_sensor_data", "created_at")
    def device_mac(self, obj):
        return obj.device.mac
    def user_username(self, obj):
        return obj.device.user.username
    device_mac.short_description = "mac address"
    user_username.short_description = 'User Username'  #
    
@admin.register(OTAUpdate)
class OTAUpdateAdmin(admin.ModelAdmin):
    list_display = ("version", "firmware_file", "created_at")


@admin.register(DevStat)
class DevStatAdmin(admin.ModelAdmin):
    list_display = ("device", "hw_version", "fw_version", "wifi_name", "wifi_password", "created_at")