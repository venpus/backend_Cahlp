from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.conf import settings
from rest_framework.authtoken.models import Token
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
import django.utils

#super user account model
class MyAccountManager(BaseUserManager):
    def create_user(self,username, email,mobile, password=None):
        if not email:
            raise ValueError("Users must have a email address")
        #if not username:
            #raise ValueError("Users must have a valid username")
        user = self.model(
            email = self.normalize_email(email),
            username = username,
            mobile = mobile,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, email, password):
        user = self.model(
            email = self.normalize_email(email),
            #username = username
        )
        user.set_password(password)
        user.is_admin = True
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.is_user = True
        user.save(using = self._db)
        return user


#Custom user model
class Account(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name='email', max_length=60, unique=True)
    username = models.CharField(verbose_name='username', max_length=60, unique=True)
    mobile = models.CharField(verbose_name = "phone" , max_length = 15, unique = False, default = True, null= True)
    first_name = models.CharField(max_length=60, default=None, null=True, blank=True)
    last_name = models.CharField(max_length=60, default=None, null=True, blank=True)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_user = models.BooleanField(default=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [email, username]
    objects = MyAccountManager()
    def __str__(self):
        return self.email
    def has_module_perms(self, app_label):
        return True


#create token for users
@receiver(post_save, sender= settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance = None, created = False, **kwargs):
    if created:
        Token.objects.create(user = instance)
        
        