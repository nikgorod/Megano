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
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='пользователь', related_name='profile')
    first_name = models.CharField(max_length=30, verbose_name='имя')
    last_name = models.CharField(max_length=30, verbose_name='фамилия')
    middle_name = models.CharField(max_length=30, verbose_name='отчество', null=True)
    balance = models.FloatField(verbose_name='баланс', default=0)
    tel = models.CharField(max_length=10, verbose_name='телефон')
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


class Manufacturer(models.Model):
    """Модель производителей"""
    name = models.CharField(max_length=20, verbose_name='производитель', db_index=True)
    category = models.ForeignKey(GoodCategory, on_delete=models.CASCADE, verbose_name='категория',
                                 related_name='manufacturer')

    class Meta:
        db_table = 'manufacturer'
        verbose_name = 'производитель'
        verbose_name_plural = 'производители'

    def __str__(self):
        return f'{self.name}'


class Specification(models.Model):
    """Модель характеристики"""
    name = models.CharField(max_length=100, verbose_name='название характеристики')
    category = models.ForeignKey(GoodCategory, on_delete=models.CASCADE, verbose_name='категория',
                                 related_name='specification')

    class Meta:
        db_table = 'specifications'
        verbose_name = 'характеристика'
        verbose_name_plural = 'характеристики'

    def __str__(self):
        return f'{self.name}'


class SpecificationValues(models.Model):
    """Модель значений характеристик"""
    specification = models.ForeignKey(Specification, on_delete=models.CASCADE, verbose_name='характеристика',
                                      related_name='specification_value')
    value = models.CharField(max_length=20, verbose_name='значение характеристики')

    class Meta:
        db_table = 'specification_values'
        verbose_name = 'значение характеристики'
        verbose_name_plural = 'значения характеристик'

    def __str__(self):
        return f'{self.specification.name} {self.value}'


class Good(models.Model):
    """Модель товара"""
    name = models.CharField(max_length=100, verbose_name='название товара', db_index=True)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)
    description = models.TextField(verbose_name='описание товара')
    category = models.ForeignKey(GoodCategory, on_delete=models.CASCADE, verbose_name='категория товара',
                                 related_name='good')
    purchases_number = models.IntegerField(verbose_name='кол-во покупок')
    release_year = models.IntegerField(verbose_name='год выпуска', default=2010)
    specifications = models.ManyToManyField(SpecificationValues)

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
    good = models.ForeignKey(Good, on_delete=models.CASCADE, verbose_name='товар', db_index=True,
                             related_name='catalog')
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, verbose_name='магазин', db_index=True)
    price = models.FloatField(default=0, verbose_name='цена на товар')
    discount = models.IntegerField(default=0, verbose_name='скидка на товар')
    count = models.IntegerField(verbose_name='кол-во товара')
    limited_edition = models.BooleanField(verbose_name='ограниченный тираж', default=False)
    purchases_number = models.PositiveIntegerField(verbose_name='кол-во покупок', default=0)

    class Meta:
        order_with_respect_to = 'good'
        db_table = 'catalog'
        verbose_name = 'каталог'
        verbose_name_plural = 'каталоги'
        indexes = [
            models.Index(fields=['good'])
        ]

    def __str__(self):
        return f'{self.good.name}, {self.shop.name}'


class Review(models.Model):
    """Модель отзывов"""
    catalog = models.ForeignKey(Catalog, on_delete=models.CASCADE, verbose_name='каталог', db_index=True,
                                related_name='reviews')
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name='пользователь')
    date = models.DateTimeField(auto_now_add=True, verbose_name='дата')
    review = models.TextField(verbose_name='отзыв')

    class Meta:
        db_table = 'reviews'
        verbose_name = 'комментарий'
        verbose_name_plural = 'комментарии'

    def __str__(self):
        return f'{self.profile.user.email}'


class CatalogImages(models.Model):
    """Модель изображений каталога"""
    catalog = models.ForeignKey(Catalog, on_delete=models.CASCADE, related_name='images', verbose_name='каталог')
    image = models.ImageField(upload_to='files/', null=True, verbose_name='изображение')

    class Meta:
        db_table = 'images'
        verbose_name = 'изображение'
        verbose_name_plural = 'изображения'


class DynamicSiteModel(models.Model):
    """Модель настроек сайта"""
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.__class__.objects.exclude(id=self.id).delete()
        super(DynamicSiteModel, self).save(*args, **kwargs)

    @classmethod
    def load(cls):
        try:
            return cls.objects.get()
        except cls.DoesNotExist:
            return cls()


class DynamicSiteSettings(DynamicSiteModel):

    """Настройки сайта"""

    title = models.CharField(max_length=256, verbose_name='title')
    meta_content = models.CharField(max_length=256, verbose_name='meta_content', default='page_content')
    cache_timeout = models.IntegerField(default=300, verbose_name='cache timeout')
    logo = models.ImageField(upload_to='site_images/', null=True, verbose_name='изображения сайта')
    express_delivery_cost = models.IntegerField(default=500, verbose_name='стоимость экспресс доставки')
    delivery_cost = models.IntegerField(default=200, verbose_name='стоимость доставки')
    order_cost = models.IntegerField(default=2000, verbose_name='стоимость заказа')

    def __str__(self):
        return 'Site Configuration'
