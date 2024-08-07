from django.contrib.auth.mixins import LoginRequiredMixin, \
    PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, \
    DeleteView
from pytils.translit import slugify

from mail_app.models import Message, Client, Newsletter, MailingAttempt


class NewsletterListView(LoginRequiredMixin, ListView):
    """ Выводит общую информацию о рассылках. """
    model = Newsletter
    paginate_by = 20

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.groups.filter(name='manager').exists():
            return Newsletter.objects.all()
        return Newsletter.objects.filter(owner=user)


class NewsletterDetailView(LoginRequiredMixin, DetailView):
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
              'periodicity', 'message', 'clients']
    success_url = reverse_lazy('mail_app:newsletter_list')

    def form_valid(self, form):
        new_newsletter = form.save(commit=False)
        new_newsletter.slug = slugify(new_newsletter.title)
        user = self.request.user
        new_newsletter.owner = user
        new_newsletter.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super().get_context_data(**kwargs)
        client_list = []
        new_client_list = []
        clients = Client.objects.filter(owner=user)
        for client in clients:
            client_list.append(client)
        for el in context['form'].fields['clients'].choices:
            if el[0].instance in client_list:
                new_client_list.append(el)
        context['form'].fields['clients'].choices = new_client_list
        return context


class NewsletterUpdateView(LoginRequiredMixin, UpdateView):
    """ Редактирует рассылку. """
    model = Newsletter
    fields = ['title', 'first_sent_at', 'last_sent_at', 'status',
              'periodicity', 'message', 'clients']
    success_url = reverse_lazy('mail_app:newsletter_list')

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super().get_context_data(**kwargs)
        client_list = []
        new_client_list = []
        clients = Client.objects.filter(owner=user)
        for client in clients:
            client_list.append(client)
        for el in context['form'].fields['clients'].choices:
            if el[0].instance in client_list:
                new_client_list.append(el)
        context['form'].fields['clients'].choices = new_client_list
        return context


class NewsletterDeleteView(LoginRequiredMixin, DeleteView):
    """ Удаляет рассылку. """
    model = Newsletter
    success_url = reverse_lazy('mail_app:newsletter_list')


class NewsletterOnOff(PermissionRequiredMixin, DetailView):
    model = Newsletter
    template_name = 'mail_app/newsletter_on_off.html'
    permission_required = 'mail_app.off_newsletter'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.status in ['Остановлена', 'Создана']:
            obj.status = 'Запущена'
        else:
            obj.status = 'Остановлена'
        obj.save()
        return obj


class MessageListView(LoginRequiredMixin, ListView):
    """ Выводит общую информацию о сообщениях. """
    model = Message
    paginate_by = 6

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.groups.filter(name='manager').exists():
            return Message.objects.all()
        return Message.objects.filter(owner=user)


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


class ClientListView(LoginRequiredMixin, ListView):
    """ Выводит общую информацию о клиентах. """
    model = Client
    paginate_by = 20

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.groups.filter(name='manager').exists():
            return Client.objects.all()
        return Client.objects.filter(owner=user)


class ClientDetailView(LoginRequiredMixin, DetailView):
    """ Выводит подробную информацию о клиенте. """
    model = Client


class ClientCreateView(LoginRequiredMixin, CreateView):
    """ Создает нового клиента. """
    model = Client
    fields = ['photo', 'email', 'name', 'surname', 'father_name', 'comment',
              'status']
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
              'status']
    success_url = reverse_lazy('mail_app:clients_list')


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    """ Удаляет клиента. """
    model = Client
    success_url = reverse_lazy('mail_app:clients_list')
