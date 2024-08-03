from django.urls import path

from mail_app.views import MessageListView, ClientListView, NewsletterListView, \
    MessageDetailView, MessageCreateView, MessageUpdateView, \
    MessageDeleteView, ClientDetailView, ClientCreateView, ClientUpdateView, \
    ClientDeleteView, NewsletterDetailView, NewsletterCreateView, \
    NewsletterUpdateView, NewsletterDeleteView, NewsletterOnOff
from .apps import MailAppConfig

app_name = MailAppConfig.name

urlpatterns = [
    path('newsletter_list/', NewsletterListView.as_view(), name='newsletter_list'),
    path('newsletters/add/', NewsletterCreateView.as_view(),
         name='newsletter_add'),
    path('newsletters/<slug:slug>/', NewsletterDetailView.as_view(),
         name='newsletter_detail'),
    path('newsletters/<slug:slug>/edit/', NewsletterUpdateView.as_view(),
         name='newsletter_edit'),
    path('newsletters/<slug:slug>/delete/', NewsletterDeleteView.as_view(),
         name='newsletter_delete'),
    path('newsletters/on_off/<slug:slug>/', NewsletterOnOff.as_view(),
         name='newsletter_on_off'),
    path('messages/', MessageListView.as_view(), name='messages_list'),
    path('messages/add/', MessageCreateView.as_view(), name='message_add'),
    path('messages/<int:pk>/', MessageDetailView.as_view(),
         name='message_detail'),
    path('messages/<int:pk>/edit/', MessageUpdateView.as_view(),
         name='message_edit'),
    path('messages/<int:pk>/delete/', MessageDeleteView.as_view(),
         name='message_delete'),
    path('clients/', ClientListView.as_view(), name='clients_list'),
    path('clients/add/', ClientCreateView.as_view(), name='client_add'),
    path('clients/<slug:slug>/', ClientDetailView.as_view(),
         name='client_detail'),
    path('clients/<slug:slug>/edit/', ClientUpdateView.as_view(),
         name='client_edit'),
    path('clients/<slug:slug>/delete/', ClientDeleteView.as_view(),
         name='client_delete')
]
