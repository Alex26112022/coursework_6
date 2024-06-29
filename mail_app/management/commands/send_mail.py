from django.core.mail import send_mail
from django.core.management import BaseCommand

from mail_app.models import Newsletter


class MailInfo:
    """ Данные рассылки. """

    def __init__(self, clients, theme, body):
        self.clients = clients
        self.theme = theme
        self.body = body


class Command(BaseCommand):
    mail_info = []
    clients_info = []

    def get_info(self):
        """ Получение информации. """

        newsletters = Newsletter.objects.filter(status='Запущена')
        clients = newsletters.prefetch_related('client')
        for el in clients:
            info = el.client.all()
            _ = []
            for item in info:
                _.append(item.email)
            self.clients_info.append(_)

        for message, clients in zip(newsletters, self.clients_info):
            self.mail_info.append(MailInfo(clients, message.message.theme,
                                           message.message.body))

    @staticmethod
    def my_send_mail(theme='my theme', body='', client_list=('123@mail.ru',)):
        """ Отправка сообщения. """
        send_mail(
            theme,
            body,
            '123@mail.ru',
            client_list,
            fail_silently=False,
        )

    def handle(self, *args, **options):
        self.get_info()
        for mail in self.mail_info:
            self.my_send_mail(mail.theme, mail.body, mail.clients)
