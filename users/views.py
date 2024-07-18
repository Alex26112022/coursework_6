import secrets

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, ListView, DetailView

from config.settings import EMAIL_HOST_USER
from users.forms import UserRegisterForm, UserProfileForm


def notification(request):
    return render(request, 'users/notification.html')


class UserCreate(CreateView):
    model = get_user_model()
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:notification')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f'http://{host}/users/email-confirm/{token}/'
        send_mail(subject='Подтверждение почты',
                  message=f'Пожалуйста, подтвердите вашу почту. '
                          f'Перейдите по ссылке: {url}',
                  from_email=EMAIL_HOST_USER,
                  recipient_list=[user.email])
        return super().form_valid(form)


class ProfileView(UpdateView):
    """ Отображает и редактирует профиль пользователя. """
    model = get_user_model()
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


class UserListView(PermissionRequiredMixin, ListView):
    """ Отображает список пользователей. """
    model = get_user_model()
    paginate_by = 20
    permission_required = 'mail_app.view_user'


class UserDetailView(PermissionRequiredMixin, DetailView):
    """ Отображает детальную информацию о пользователе. """
    model = get_user_model()
    permission_required = 'mail_app.view_user'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.is_active = not obj.is_active
        obj.save()
        return obj
