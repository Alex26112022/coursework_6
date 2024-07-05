import smtplib
import csv
import os

from django.core.mail import send_mail
from django.utils import timezone

from config import settings
from mail_app.models import Newsletter, MailingAttempt
from my_config import path_csv

now = timezone.now().date()


def write_csv(csv_file, pk_, send_, email_, message_, time_, success_,
              answer_):
    """ Записывает в CSV файл данные по попыткам рассылок. """
    if not os.path.exists(csv_file):
        with open(csv_file, 'w', encoding='utf8', newline='') as csvfile:
            fieldnames = ['ID', 'РАССЫЛКА', 'EMAIL', 'СООБЩЕНИЕ',
                          'ВРЕМЯ ПОПЫТКИ', 'УСПЕШНОСТЬ', 'ОТВЕТ СЕРВЕРА']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            writer.writerow({'ID': pk_, 'РАССЫЛКА': send_, 'EMAIL': email_,
                             'СООБЩЕНИЕ': message_, 'ВРЕМЯ ПОПЫТКИ': time_,
                             'УСПЕШНОСТЬ': success_, 'ОТВЕТ СЕРВЕРА': answer_})

    else:
        with open(csv_file, 'a', encoding='utf8', newline='') as csvfile:
            fieldnames = ['ID', 'РАССЫЛКА', 'EMAIL', 'СООБЩЕНИЕ',
                          'ВРЕМЯ ПОПЫТКИ', 'УСПЕШНОСТЬ', 'ОТВЕТ СЕРВЕРА']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writerow({'ID': pk_, 'РАССЫЛКА': send_, 'EMAIL': email_,
                             'СООБЩЕНИЕ': message_, 'ВРЕМЯ ПОПЫТКИ': time_,
                             'УСПЕШНОСТЬ': success_, 'ОТВЕТ СЕРВЕРА': answer_})


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
            write_csv(path_csv, newsletter.pk, newsletter.title, clients_list,
                      newsletter.message, attempt.last_attempt_at,
                      attempt.successfully, attempt.mail_response)


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
                write_csv(path_csv, newsletter.pk, newsletter.title,
                          clients_list,
                          newsletter.message, attempt.last_attempt_at,
                          attempt.successfully, attempt.mail_response)


def my_send_status():
    """ Проверяет актуальность статуса рассылки. """
    newsletters = Newsletter.objects.filter(last_sent_at__lt=now)
    for newsletter in newsletters:
        newsletter.status = 'Остановлена'
        newsletter.save()
    print('Статусы обновлены')
