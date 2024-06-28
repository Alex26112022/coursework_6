from django.db import models
from pytils.translit import slugify

optional = {'blank': True, 'null': True}


class Client(models.Model):
    status_list = [('Активный', 'Активный'), ('Неактивный', 'Неактивный'),
                   ('Новый', 'Новый'), ('Потенциальный', 'Потенциальный'),
                   ('Заблокированный', 'Заблокированный'),
                   ('Неизвестный', 'Неизвестный')]
    photo = models.ImageField(upload_to='mail_app/clients/',
                              verbose_name='Фото', **optional)
    email = models.EmailField(unique=True, verbose_name='Email', db_index=True)
    slug = models.SlugField(max_length=255, verbose_name='Слаг', **optional)
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

    title = models.CharField(max_length=255, verbose_name='Название рассылки')
    slug = models.SlugField(max_length=255, verbose_name='Слаг', **optional)
    first_sent_at = models.DateTimeField(
        verbose_name='Дата первого отправления', **optional)
    status = models.CharField(max_length=255, choices=status_list,
                              default='Создана', verbose_name='Статус')
    periodicity = models.CharField(max_length=255,
                                   verbose_name='Периодичность', **optional)
    count_sent = models.IntegerField(verbose_name='Количество отправленных',
                                     **optional)
    count_delivered = models.IntegerField(
        verbose_name='Количество доставленных', **optional)
    count_transition = models.IntegerField(verbose_name='Количество переходов',
                                           **optional)
    message = models.ForeignKey('Message', on_delete=models.SET_NULL,
                                related_name='newsletter',
                                verbose_name='Сообщение', **optional)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'
        ordering = ['title']


class Message(models.Model):
    theme = models.CharField(max_length=255, verbose_name='Тема сообщения',
                             **optional)
    body = models.TextField(verbose_name='Текст сообщения', **optional)
    image = models.ImageField(upload_to='mail_app/messages/',
                              verbose_name='Изображение', **optional)

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
