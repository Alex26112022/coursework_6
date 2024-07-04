from django.core.mail import send_mail
from django.utils import timezone

from mail_app.models import Newsletter

now = timezone.now().date()


def my_send_mail():
    """ Мгновенно запускает рассылку, если она попадает в диапазон дат. """

    newsletters = Newsletter.objects.filter(status='Запущена',
                                            first_sent_at__lte=now,
                                            last_sent_at__gte=now)

    for newsletter in newsletters:
        clients_list = []
        for el in newsletter.client.all():
            if el.status != 'Заблокированный':
                clients_list.append(el.email)

        send_mail(newsletter.message.theme, newsletter.message.body,
                  '123@mail.ru', clients_list, fail_silently=False)


def my_period_mail():
    """ Периодический запуск рассылок. """
    newsletters = Newsletter.objects.filter(status='Запущена',
                                            first_sent_at__lte=now,
                                            last_sent_at__gte=now)

    for newsletter in newsletters:
        if newsletter.periodicity == 'День' or newsletter.periodicity == 'Неделя' and (
                now - newsletter.first_sent_at).days % 7 == 0 or newsletter.periodicity == 'Месяц' and (
                now - newsletter.first_sent_at).days % 30 == 0 or newsletter.periodicity == 'Год' and (
                now - newsletter.first_sent_at).days % 365 == 0:

            clients_list = []
            for el in newsletter.client.all():
                if el.status != 'Заблокированный':
                    clients_list.append(el.email)

            send_mail(newsletter.message.theme, newsletter.message.body,
                      '123@mail.ru', clients_list, fail_silently=False)
