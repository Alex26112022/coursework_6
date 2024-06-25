from django.shortcuts import render
from django.views.generic import ListView

from mail_app.models import Message, Client, Newsletter


class NewsletterListView(ListView):
    model = Newsletter
    paginate_by = 20


class MessageListView(ListView):
    model = Message
    paginate_by = 6


class ClientListView(ListView):
    model = Client
    paginate_by = 20
