from django.urls import path

from mail_app.views import MessageListView, ClientListView, NewsletterListView
from .apps import MailAppConfig

app_name = MailAppConfig.name

urlpatterns = [
    path('', NewsletterListView.as_view(), name='newsletter_list'),
    path('messages/', MessageListView.as_view(), name='messages_list'),
    path('clients/', ClientListView.as_view(), name='clients_list'),
]
