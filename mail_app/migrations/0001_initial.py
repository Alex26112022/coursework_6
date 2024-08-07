# Generated by Django 5.0.6 on 2024-06-25 13:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('theme', models.CharField(blank=True, max_length=255, null=True, verbose_name='Тема сообщения')),
                ('body', models.TextField(blank=True, null=True, verbose_name='Текст сообщения')),
                ('image', models.ImageField(blank=True, null=True, upload_to='mail_app/messages/', verbose_name='Изображение')),
            ],
            options={
                'verbose_name': 'Сообщение',
                'verbose_name_plural': 'Сообщения',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Newsletter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Название рассылки')),
                ('first_sent_at', models.DateTimeField(blank=True, null=True, verbose_name='Дата первого отправления')),
                ('status', models.CharField(choices=[('CREATE', 'Создана'), ('START', 'Запущена'), ('STOP', 'Остановлена')], default='CREATE', max_length=255, verbose_name='Статус')),
                ('periodicity', models.CharField(blank=True, max_length=255, null=True, verbose_name='Периодичность')),
                ('count_sent', models.IntegerField(blank=True, null=True, verbose_name='Количество отправленных')),
                ('count_delivered', models.IntegerField(blank=True, null=True, verbose_name='Количество доставленных')),
                ('count_transition', models.IntegerField(blank=True, null=True, verbose_name='Количество переходов')),
                ('message', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='mail_app.message')),
            ],
            options={
                'verbose_name': 'Рассылка',
                'verbose_name_plural': 'Рассылки',
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='MailingAttempt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_attempt_at', models.DateTimeField(auto_now=True, verbose_name='Последняя попытка отправки')),
                ('successfully', models.BooleanField(default=False, verbose_name='Успешно?')),
                ('mail_response', models.CharField(blank=True, max_length=255, null=True, verbose_name='Ответ сервера')),
                ('newsletter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mail_app.newsletter')),
            ],
            options={
                'verbose_name': 'Попытка отправки рассылки',
                'verbose_name_plural': 'Попытки отправки рассылок',
                'ordering': ['-last_attempt_at'],
            },
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='mail_app/clients/', verbose_name='Фото')),
                ('email', models.EmailField(db_index=True, max_length=254, unique=True, verbose_name='Email')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='Имя')),
                ('surname', models.CharField(blank=True, max_length=255, null=True, verbose_name='Фамилия')),
                ('father_name', models.CharField(blank=True, max_length=255, null=True, verbose_name='Отчество')),
                ('comment', models.TextField(blank=True, null=True, verbose_name='Комментарий')),
                ('status', models.CharField(choices=[('ACTIVE', 'Активный'), ('INACTIVE', 'Неактивный'), ('NEW', 'Новый'), ('POTENTIAL', 'Потенциальный'), ('BLOCKED', 'Заблокированный'), ('UNKNOWN', 'Неизвестный')], default='UNKNOWN', max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')),
                ('last_link_click', models.DateTimeField(blank=True, null=True, verbose_name='Последний переход по ссылке')),
                ('newsletter', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='mail_app.newsletter', verbose_name='Рассылка')),
            ],
            options={
                'verbose_name': 'Клиент',
                'verbose_name_plural': 'Клиенты',
                'ordering': ['-created_at'],
            },
        ),
    ]
