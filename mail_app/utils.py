from datetime import timedelta

from django.core.mail import send_mail
from django.utils import timezone

from mail_app.models import Newsletter

now = timezone.now()


def my_send_mail():
    """ Получение информации. """
    mail_info = []
    clients_info = []

    newsletters = Newsletter.objects.filter(status='Запущена',
                                            first_sent_at__lt=now,
                                            last_sent_at__gte=now + timedelta(
                                                minutes=5))

    for newsletter in newsletters:
        clients_list = []
        for el in newsletter.client.all():
            if el.status != 'Заблокированный':
                clients_list.append(el.email)

        send_mail(newsletter.message.theme, newsletter.message.body,
                  '123@mail.ru', clients_list, fail_silently=False)
