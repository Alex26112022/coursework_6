from django.core.mail import send_mail
from django.utils import timezone

from mail_app.models import Newsletter

now = timezone.now()


class MailInfo:
    """ Данные рассылки. """

    def __init__(self, clients, theme, body):
        self.clients = clients
        self.theme = theme
        self.body = body


def get_info():
    """ Получение информации. """
    mail_info = []
    clients_info = []

    newsletters = Newsletter.objects.filter(status='Запущена',
                                            first_sent_at__lt=now,
                                            last_sent_at__gt=now)
    clients = newsletters.prefetch_related('client')
    for el in clients:
        info = el.client.all()
        _ = []
        for item in info:
            _.append(item.email)
        clients_info.append(_)

    for message, clients in zip(newsletters, clients_info):
        mail_info.append(MailInfo(clients, message.message.theme,
                                  message.message.body))

    return mail_info


def my_send_mail(theme='my theme', body='', client_list=('123@mail.ru',)):
    """ Отправка сообщения. """
    send_mail(
        theme,
        body,
        '123@mail.ru',
        client_list,
        fail_silently=False,
    )


def main_mail():
    for mail in get_info():
        my_send_mail(mail.theme, mail.body, mail.clients)
