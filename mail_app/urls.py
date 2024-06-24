from django.urls import path

from mail_app.views import index
from .apps import MailAppConfig

app_name = MailAppConfig.name

urlpatterns = [
    path('', index, name='mail_list'),
]
