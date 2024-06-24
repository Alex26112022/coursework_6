from django.urls import path

from mail_app.views import index, examples, client
from .apps import MailAppConfig

app_name = MailAppConfig.name

urlpatterns = [
    path('', index, name='mail_list'),
    path('examples/', examples, name='examples'),
    path('clients/', client, name='clients'),
]
