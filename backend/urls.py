from django.urls import path
from backend.views import UserRegistrationView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-registration'),
]