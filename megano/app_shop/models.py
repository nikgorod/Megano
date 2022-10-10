from django.db import models
from django.contrib.auth.models import User


class GoodCategory(models.Model):
    name = models.CharField(max_length=30, unique=True, db_index=True, verbose_name='категории товара')
    active_goods = models.BooleanField(verbose_name='активные товары')

    class Meta:
        db_table = 'good_category'
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return f'{self.name}'


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='пользователь')
    first_name = models.CharField(max_length=30, verbose_name='имя')
    last_name = models.CharField(max_length=30, verbose_name='фамилия')
    middle_name = models.CharField(max_length=30, verbose_name='отчество')
    email = models.CharField(max_length=40, verbose_name='email', unique=True)
    balance = models.FloatField(verbose_name='баланс', default=0)
    tel = models.CharField(max_length=18, verbose_name='телефон')
    avatar = models.ImageField(upload_to='files/', verbose_name='аватар пользователя')

    class Meta:
        db_table = 'user_profile'
        verbose_name = 'профиль пользователя'
        verbose_name_plural = 'профили пользователей'


class Shop(models.Model):
    name = models.CharField(max_length=50, verbose_name='название магазина', db_index=True)
    description = models.TextField(verbose_name='описание магазина')

    class Meta:
        db_table = 'shops'
        verbose_name_plural = 'магазины'
        verbose_name = 'магазин'

    def __str__(self):
        return f'{self.name}'
