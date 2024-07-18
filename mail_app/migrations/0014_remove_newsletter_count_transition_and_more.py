# Generated by Django 4.2 on 2024-07-18 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mail_app', '0013_alter_newsletter_count_delivered_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='newsletter',
            name='count_transition',
        ),
        migrations.AddField(
            model_name='message',
            name='views_count',
            field=models.PositiveIntegerField(default=0, verbose_name='Количество переходов'),
        ),
    ]