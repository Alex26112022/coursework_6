from django.db import models
from django.utils import timezone

from users.models import User

optional = {'blank': True, 'null': True}


class Client(models.Model):
    status_list = [('Активный', 'Активный'), ('Неактивный', 'Неактивный'),
                   ('Новый', 'Новый'), ('Потенциальный', 'Потенциальный'),
                   ('Заблокированный', 'Заблокированный'),
                   ('Неизвестный', 'Неизвестный')]
    photo = models.ImageField(upload_to='mail_app/clients/',
                              verbose_name='Фото', **optional)
    email = models.EmailField(unique=True, verbose_name='Email', db_index=True)
    slug = models.SlugField(max_length=255, verbose_name='Слаг', unique=True)
    name = models.CharField(max_length=255, verbose_name='Имя', **optional)
    surname = models.CharField(max_length=255, verbose_name='Фамилия',
                               **optional)
    father_name = models.CharField(max_length=255, verbose_name='Отчество',
                                   **optional)
    comment = models.TextField(verbose_name='Комментарий', **optional)
    status = models.CharField(max_length=255, choices=status_list,
                              default='Неизвестный')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата '
                                                                      'добавления')
    last_link_click = models.DateTimeField(
        verbose_name='Последний переход по ссылке', **optional)
    newsletter = models.ForeignKey('Newsletter', on_delete=models.SET_NULL,
                                   verbose_name='Рассылка',
                                   related_name='client', **optional)
    owner = models.ForeignKey(User, blank=True, null=True,
                              verbose_name='Владелец',
                              on_delete=models.SET_NULL,
                              related_name='client')

    def __str__(self):
        return f'{self.surname} {self.name} {self.father_name}'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'
        ordering = ['-created_at']


class Newsletter(models.Model):
    status_list = [('Создана', 'Создана'),
                   ('Запущена', 'Запущена'),
                   ('Остановлена', 'Остановлена')]

    periodicity_list = [('День', 'День'), ('Неделя', 'Неделя'),
                        ('Месяц', 'Месяц'), ('Год', 'Год')]

    title = models.CharField(max_length=255, verbose_name='Название рассылки',
                             unique=True)
    slug = models.SlugField(max_length=255, verbose_name='Слаг', unique=True)
    first_sent_at = models.DateField(
        verbose_name='Дата первого отправления', default=timezone.now)
    last_sent_at = models.DateField(
        verbose_name='Дата крайнего отправления', default=timezone.now)
    status = models.CharField(max_length=255, choices=status_list,
                              default='Создана', verbose_name='Статус')
    periodicity = models.CharField(max_length=255,
                                   verbose_name='Периодичность',
                                   choices=periodicity_list, default='Год')
    count_sent = models.IntegerField(verbose_name='Количество отправленных',
                                     default=0)
    count_delivered = models.IntegerField(
        verbose_name='Количество доставленных', default=0)
    message = models.ForeignKey('Message', on_delete=models.SET_NULL,
                                related_name='newsletter',
                                verbose_name='Сообщение', **optional)
    owner = models.ForeignKey(User, blank=True, null=True,
                              verbose_name='Владелец',
                              on_delete=models.SET_NULL,
                              related_name='newsletter')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'
        ordering = ['title']
        permissions = [
            ('view_user', 'Просматривать список пользователей сервиса'),
            ('block_user', 'Блокировать пользователей сервиса'),
            ('off_newsletter', 'Отключать рассылки')
        ]


class Message(models.Model):
    theme = models.CharField(max_length=255, verbose_name='Тема сообщения',
                             **optional)
    body = models.TextField(verbose_name='Текст сообщения', **optional)
    image = models.ImageField(upload_to='mail_app/messages/',
                              verbose_name='Изображение', **optional)
    views_count = models.PositiveIntegerField(
        verbose_name='Количество переходов', default=0)
    owner = models.ForeignKey(User, blank=True, null=True,
                              verbose_name='Владелец',
                              on_delete=models.SET_NULL,
                              related_name='message')

    def __str__(self):
        return self.theme

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
        ordering = ['id']


class MailingAttempt(models.Model):
    last_attempt_at = models.DateTimeField(auto_now=True,
                                           verbose_name='Последняя попытка '
                                                        'отправки')
    successfully = models.BooleanField(default=False, verbose_name='Успешно?')
    mail_response = models.CharField(max_length=255,
                                     verbose_name='Ответ сервера', **optional)
    newsletter = models.ForeignKey('Newsletter', on_delete=models.CASCADE,
                                   verbose_name='Рассылка',
                                   related_name='attempt')

    def __str__(self):
        return f'{self.last_attempt_at} {self.successfully} {self.mail_response}'

    class Meta:
        verbose_name = 'Попытка отправки рассылки'
        verbose_name_plural = 'Попытки отправки рассылок'
        ordering = ['-last_attempt_at']
