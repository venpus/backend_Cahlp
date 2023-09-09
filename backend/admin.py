from backend.models.usermodel import Account
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin

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
admin.site.register(Account, CustomUserAdmin)