from django.contrib.auth.models import AbstractUser
from django.db import models

from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='E-mail')
    photo = models.ImageField(verbose_name='Фото', upload_to='users/',
                              blank=True, null=True)
    phone = PhoneNumberField(region='RU', verbose_name='Телефон', blank=True,
                             null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email
