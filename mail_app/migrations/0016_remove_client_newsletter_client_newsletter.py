# Generated by Django 4.2 on 2024-08-01 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mail_app', '0015_alter_newsletter_options_client_owner_message_owner_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='client',
            name='newsletter',
        ),
        migrations.AddField(
            model_name='client',
            name='newsletter',
            field=models.ManyToManyField(related_name='client', to='mail_app.newsletter', verbose_name='Рассылка'),
        ),
    ]
