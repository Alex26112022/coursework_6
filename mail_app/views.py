from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, \
    DeleteView
from pytils.translit import slugify

from mail_app.models import Message, Client, Newsletter, MailingAttempt


class NewsletterListView(ListView):
    model = Newsletter
    paginate_by = 20


class NewsletterDetailView(DetailView):
    model = Newsletter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        clients = Client.objects.filter(newsletter=self.object)
        attempts = MailingAttempt.objects.filter(newsletter=self.object)
        context['clients'] = clients
        context['attempts'] = attempts
        return context


class NewsletterCreateView(CreateView):
    model = Newsletter
    fields = ['title', 'status', 'periodicity', 'message']
    success_url = reverse_lazy('mail_app:newsletter_list')

    def form_valid(self, form):
        new_newsletter = form.save(commit=False)
        new_newsletter.slug = slugify(new_newsletter.title)
        new_newsletter.save()
        return super().form_valid(form)


class NewsletterUpdateView(UpdateView):
    model = Newsletter
    fields = ['title', 'status', 'periodicity', 'message']
    success_url = reverse_lazy('mail_app:newsletter_list')


class NewsletterDeleteView(DeleteView):
    model = Newsletter
    success_url = reverse_lazy('mail_app:newsletter_list')


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
              'status', 'newsletter']
    success_url = reverse_lazy('mail_app:clients_list')

    def form_valid(self, form):
        new_client = form.save(commit=False)
        new_client.slug = slugify(new_client.email)
        new_client.save()
        return super().form_valid(form)


class ClientUpdateView(UpdateView):
    model = Client
    fields = ['photo', 'email', 'name', 'surname', 'father_name', 'comment',
              'status', 'newsletter']
    success_url = reverse_lazy('mail_app:clients_list')


class ClientDeleteView(DeleteView):
    model = Client
    success_url = reverse_lazy('mail_app:clients_list')
