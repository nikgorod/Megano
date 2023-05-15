from django.db import models

from app_shop.models import Catalog, User


class Delivery(models.Model):
    """МОдель доставки"""
    DELIVERY_CHOICES = (
        ('1', 'Обычная доставка'),
        ('2', 'Экспресс-доставка ')
    )
    delivery_type = models.CharField(verbose_name='тип доставки', choices=DELIVERY_CHOICES, max_length=50)
    city = models.CharField(max_length=50, verbose_name='город доставки')
    address = models.TextField(verbose_name='адрес доставки')
    delivery_cost = models.IntegerField(verbose_name='стоимость доставки')

    class Meta:
        db_table = 'delivery'
        verbose_name = 'доставка'
        verbose_name_plural = 'доставки'

    def __str__(self):
        return f'{self.delivery_cost}'


class Payment(models.Model):
    """Модель способа оплаты"""
    PAYMENT_CHOICES = (
        ('1', 'Онлайн картой'),
        ('2', 'Онлайн со случайного чужого счёта'),
    )
    code = models.CharField(max_length=30, verbose_name='статус оплаты')
    card_num = models.CharField(max_length=9, verbose_name='номер карты')
    payment_type = models.CharField(verbose_name='способ оплаты', choices=PAYMENT_CHOICES, max_length=50)

    class Meta:
        db_table = 'payment'
        verbose_name = 'оплата'

    def __str__(self):
        return f'{self.code}'


class Order(models.Model):
    """Модель заказа"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь')
    date = models.DateTimeField(verbose_name='дата заказа', auto_now=True)
    amount = models.IntegerField(verbose_name='общая сумма заказа')
    delivery = models.ForeignKey(Delivery, related_name='order', on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, related_name='order', on_delete=models.CASCADE)

    class Meta:
        db_table = 'orders'
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'


class OrdersToGoods(models.Model):
    """Заказы к товарам"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_to_good')
    good = models.ForeignKey(Catalog, on_delete=models.CASCADE, related_name='good_to_order')
    quantity = models.IntegerField(verbose_name='кол-во товара')

    class Meta:
        db_table = 'orders_to_good'
