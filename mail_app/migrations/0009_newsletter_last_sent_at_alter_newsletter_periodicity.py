# Generated by Django 5.0.6 on 2024-07-04 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mail_app', '0008_alter_newsletter_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='newsletter',
            name='last_sent_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Дата крайнего отправления'),
        ),
        migrations.AlterField(
            model_name='newsletter',
            name='periodicity',
            field=models.CharField(blank=True, choices=[('День', 'День'), ('Неделя', 'Неделя'), ('Месяц', 'Месяц'), ('Год', 'Год')], default='Год', max_length=255, null=True, verbose_name='Периодичность'),
        ),
    ]
