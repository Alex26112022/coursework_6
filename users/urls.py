from django.urls import path

from users.apps import UsersConfig
from users.utils import email_verification
from users.views import UserCreate, notification

app_name = UsersConfig.name

urlpatterns = [
    path('register/', UserCreate.as_view(), name='register'),
    path('email-confirm/<str:token>/', email_verification,
         name='email-confirm'),
    path('notification/', notification, name='notification'),
]
