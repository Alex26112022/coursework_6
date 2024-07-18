from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, \
    DeleteView
from pytils.translit import slugify

from mail_app.models import Message, Client, Newsletter, MailingAttempt


class NewsletterListView(ListView):
    """ Выводит общую информацию о рассылках. """
    model = Newsletter
    paginate_by = 20


class NewsletterDetailView(DetailView):
    """ Выводит подробную информацию о рассылке. """
    model = Newsletter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        clients = Client.objects.filter(newsletter=self.object)
        attempts = MailingAttempt.objects.filter(newsletter=self.object)
        context['clients'] = clients
        context['attempts'] = attempts
        return context


class NewsletterCreateView(LoginRequiredMixin, CreateView):
    """ Создает новую рассылку. """
    model = Newsletter
    fields = ['title', 'first_sent_at', 'last_sent_at', 'status',
              'periodicity', 'message']
    success_url = reverse_lazy('mail_app:newsletter_list')

    def form_valid(self, form):
        new_newsletter = form.save(commit=False)
        new_newsletter.slug = slugify(new_newsletter.title)
        user = self.request.user
        new_newsletter.owner = user
        new_newsletter.save()
        return super().form_valid(form)


class NewsletterUpdateView(LoginRequiredMixin, UpdateView):
    """ Редактирует рассылку. """
    model = Newsletter
    fields = ['title', 'first_sent_at', 'last_sent_at', 'status',
              'periodicity', 'message']
    success_url = reverse_lazy('mail_app:newsletter_list')


class NewsletterDeleteView(LoginRequiredMixin, DeleteView):
    """ Удаляет рассылку. """
    model = Newsletter
    success_url = reverse_lazy('mail_app:newsletter_list')


class MessageListView(ListView):
    """ Выводит общую информацию о сообщениях. """
    model = Message
    paginate_by = 6


class MessageDetailView(DetailView):
    """ Выводит подробную информацию о сообщении. """
    model = Message

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if not self.request.user.is_authenticated:
            obj.views_count += 1
        obj.save()
        return obj


class MessageCreateView(LoginRequiredMixin, CreateView):
    """ Создает новое сообщение. """
    model = Message
    fields = ['theme', 'body', 'image']
    success_url = reverse_lazy('mail_app:messages_list')

    def form_valid(self, form):
        message = form.save(commit=False)
        user = self.request.user
        message.owner = user
        message.save()
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    """ Редактирует сообщение. """
    model = Message
    fields = ['theme', 'body', 'image']
    success_url = reverse_lazy('mail_app:messages_list')


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    """ Удаляет сообщение. """
    model = Message
    success_url = reverse_lazy('mail_app:messages_list')


class ClientListView(ListView):
    """ Выводит общую информацию о клиентах. """
    model = Client
    paginate_by = 20


class ClientDetailView(DetailView):
    """ Выводит подробную информацию о клиенте. """
    model = Client


class ClientCreateView(LoginRequiredMixin, CreateView):
    """ Создает нового клиента. """
    model = Client
    fields = ['photo', 'email', 'name', 'surname', 'father_name', 'comment',
              'status', 'newsletter']
    success_url = reverse_lazy('mail_app:clients_list')

    def form_valid(self, form):
        new_client = form.save(commit=False)
        new_client.slug = slugify(new_client.email)
        user = self.request.user
        new_client.owner = user
        new_client.save()
        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    """ Редактирует клиента. """
    model = Client
    fields = ['photo', 'email', 'name', 'surname', 'father_name', 'comment',
              'status', 'newsletter']
    success_url = reverse_lazy('mail_app:clients_list')


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    """ Удаляет клиента. """
    model = Client
    success_url = reverse_lazy('mail_app:clients_list')
