from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse


def email_verification(request, token):
    """ Проверка почты. """
    user = get_object_or_404(get_user_model(), token=token)
    user.is_active = True
    user.save()
    return redirect(reverse('mail_app:newsletter_list'))
