# Generated by Django 5.0.6 on 2024-06-28 13:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mail_app', '0005_alter_client_status_alter_newsletter_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='slug',
            field=models.SlugField(blank=True, max_length=255, null=True, verbose_name='Слаг'),
        ),
        migrations.AddField(
            model_name='newsletter',
            name='slug',
            field=models.SlugField(blank=True, max_length=255, null=True, verbose_name='Слаг'),
        ),
        migrations.AlterField(
            model_name='newsletter',
            name='message',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='newsletter', to='mail_app.message', verbose_name='Сообщение'),
        ),
    ]