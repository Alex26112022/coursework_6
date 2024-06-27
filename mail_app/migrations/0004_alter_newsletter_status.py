# Generated by Django 5.0.6 on 2024-06-25 18:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mail_app', '0003_alter_newsletter_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newsletter',
            name='status',
            field=models.CharField(choices=[('CREATE', 'Создана'), ('START', 'Запущена'), ('STOP', 'Остановлена')], default='CREATE', max_length=255, verbose_name='Статус'),
        ),
    ]
