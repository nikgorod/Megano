from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractUser


class UserManager(BaseUserManager):
    """Модель User без использования username"""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Создание пользователя с email и password"""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """User model."""

    username = None
    email = models.EmailField('email address', unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email


class UserProfile(models.Model):
    """Расширенная модель пользователя"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='пользователь')
    first_name = models.CharField(max_length=30, verbose_name='имя')
    last_name = models.CharField(max_length=30, verbose_name='фамилия')
    middle_name = models.CharField(max_length=30, verbose_name='отчество', null=True)
    balance = models.FloatField(verbose_name='баланс', default=0)
    tel = models.CharField(max_length=18, verbose_name='телефон')
    avatar = models.ImageField(upload_to='files/', verbose_name='аватар пользователя')

    class Meta:
        db_table = 'user_profile'
        verbose_name = 'профиль пользователя'
        verbose_name_plural = 'профили пользователей'

    def __str__(self):
        return self.user.email


class Shop(models.Model):
    """Модель магазина"""
    name = models.CharField(max_length=50, verbose_name='название магазина', db_index=True)
    description = models.TextField(verbose_name='описание магазина')

    class Meta:
        db_table = 'shops'
        verbose_name_plural = 'магазины'
        verbose_name = 'магазин'

    def __str__(self):
        return f'{self.name}'


class GoodCategory(models.Model):
    """Модель категорий товара"""
    name = models.CharField(max_length=30, unique=True, db_index=True, verbose_name='категории товара')
    active_goods = models.BooleanField(verbose_name='активные товары')

    class Meta:
        db_table = 'good_category'
        verbose_name = 'категория'
        verbose_name_plural = 'категории'
        indexes = [
            models.Index(fields=['name'])
        ]

    def __str__(self):
        return f'{self.name}'


class Good(models.Model):
    """Модель товара"""
    name = models.CharField(max_length=100, verbose_name='название товара', db_index=True)
    description = models.TextField(verbose_name='описание товара')
    category = models.ForeignKey(GoodCategory, on_delete=models.CASCADE, verbose_name='категория товара')

    class Meta:
        db_table = 'good'
        verbose_name = 'товар'
        verbose_name_plural = 'товары'
        indexes = [
            models.Index(fields=['category'])
        ]

    def __str__(self):
        return f'{self.name}'


class GoodTags(models.Model):
    """Модель тегов к товарам"""
    name = models.CharField(max_length=30, verbose_name='название тега')
    tags_to_good = models.ManyToManyField(Good, verbose_name='теги к товарам')

    class Meta:
        db_table = 'tags'
        verbose_name = 'тег'
        verbose_name_plural = 'теги'

    def __str__(self):
        return f'{self.name}'


class Catalog(models.Model):
    """Модель каталога"""
    good = models.ForeignKey(Good, on_delete=models.CASCADE, verbose_name='товар', db_index=True)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, verbose_name='магазин', db_index=True)
    price = models.FloatField(default=0, verbose_name='цена на товар')
    discount = models.IntegerField(default=0, verbose_name='скидка на товар')
    count = models.IntegerField(verbose_name='кол-во товара')

    class Meta:
        db_table = 'catalog'
        verbose_name = 'каталог'
        verbose_name_plural = 'каталоги'
        indexes = [
            models.Index(fields=['good'])
        ]

    def __str__(self):
        return f'{self.good.name}, {self.shop.name}'


class CatalogImages(models.Model):
    """Модель изображений каталога"""
    catalog = models.ForeignKey(Catalog, on_delete=models.CASCADE, related_name='images', verbose_name='каталог')
    image = models.ImageField(upload_to='files/', null=True, verbose_name='изображение')

    class Meta:
        db_table = 'images'
        verbose_name = 'изображение'
        verbose_name_plural = 'изображения'
