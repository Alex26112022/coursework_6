import smtplib

from django.core.mail import send_mail
from django.utils import timezone

from config import settings
from mail_app.models import Newsletter, MailingAttempt

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

        try:
            response = send_mail(newsletter.message.theme,
                                 newsletter.message.body,
                                 settings.EMAIL_HOST_USER, clients_list,
                                 fail_silently=False)

            attempt = MailingAttempt.objects.create(newsletter=newsletter,
                                                    successfully=True,
                                                    mail_response=str(
                                                        response))

        except smtplib.SMTPException as e:
            attempt = MailingAttempt.objects.create(newsletter=newsletter,
                                                    successfully=False,
                                                    mail_response=str(e))

            print(f'Ошибка при отправке рассылки {newsletter.title}: {str(e)}')

        else:
            newsletter.count_delivered += 1
            newsletter.save()
            print(f'Отправлена рассылка {newsletter.title}')

        finally:
            newsletter.count_sent += 1
            newsletter.save()


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

            try:
                response = send_mail(newsletter.message.theme,
                                     newsletter.message.body,
                                     settings.EMAIL_HOST_USER, clients_list,
                                     fail_silently=False)

                attempt = MailingAttempt.objects.create(newsletter=newsletter,
                                                        successfully=True,
                                                        mail_response=str(
                                                            response))

            except smtplib.SMTPException as e:
                attempt = MailingAttempt.objects.create(newsletter=newsletter,
                                                        successfully=False,
                                                        mail_response=str(e))

                print(
                    f'Ошибка при отправке рассылки {newsletter.title}: {str(e)}')

            else:
                newsletter.count_delivered += 1
                newsletter.save()
                print(f'Отправлена рассылка {newsletter.title}')

            finally:
                newsletter.count_sent += 1
                newsletter.save()


def my_send_status():
    """ Проверяет актуальность статуса рассылки. """
    newsletters = Newsletter.objects.filter(last_sent_at__lt=now)
    for newsletter in newsletters:
        newsletter.status = 'Остановлена'
        newsletter.save()
    print('Статусы обновлены')
