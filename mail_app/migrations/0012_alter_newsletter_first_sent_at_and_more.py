# Generated by Django 5.0.6 on 2024-07-04 17:30

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mail_app', '0011_alter_newsletter_first_sent_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newsletter',
            name='first_sent_at',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='Дата первого отправления'),
        ),
        migrations.AlterField(
            model_name='newsletter',
            name='last_sent_at',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='Дата крайнего отправления'),
        ),
    ]
