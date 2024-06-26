from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, \
    DeleteView

from mail_app.models import Message, Client, Newsletter


class NewsletterListView(ListView):
    model = Newsletter
    paginate_by = 20


class MessageListView(ListView):
    model = Message
    paginate_by = 6


class MessageDetailView(DetailView):
    model = Message


class MessageCreateView(CreateView):
    model = Message
    fields = '__all__'
    success_url = reverse_lazy('mail_app:messages_list')


class MessageUpdateView(UpdateView):
    model = Message
    fields = '__all__'
    success_url = reverse_lazy('mail_app:messages_list')


class MessageDeleteView(DeleteView):
    model = Message
    success_url = reverse_lazy('mail_app:messages_list')


class ClientListView(ListView):
    model = Client
    paginate_by = 20


class ClientDetailView(DetailView):
    model = Client


class ClientCreateView(CreateView):
    model = Client
    fields = ['photo', 'email', 'name', 'surname', 'father_name', 'comment',
              'status']
    success_url = reverse_lazy('mail_app:clients_list')


class ClientUpdateView(UpdateView):
    model = Client
    fields = ['photo', 'email', 'name', 'surname', 'father_name', 'comment',
              'status']
    success_url = reverse_lazy('mail_app:clients_list')


class ClientDeleteView(DeleteView):
    model = Client
    success_url = reverse_lazy('mail_app:clients_list')
