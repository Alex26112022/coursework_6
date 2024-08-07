# Generated by Django 4.2 on 2024-08-02 08:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_index=True, max_length=200, unique=True, verbose_name='Заголовок')),
                ('information', models.TextField(blank=True, null=True, verbose_name='Содержимое статьи')),
                ('image', models.ImageField(blank=True, null=True, upload_to='', verbose_name='Изображение')),
                ('count_view', models.IntegerField(default=0, verbose_name='Количество просмотров')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')),
            ],
        ),
    ]
