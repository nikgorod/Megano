from decimal import Decimal

from django.conf import settings

from app_shop.models import Catalog


class Cart(object):

    def __init__(self, request):
        """
        Инициализация корзины
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # сохраняем ПУСТУЮ корзину в сессии
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def __iter__(self):
        """
        Перебираем товары в корзине и получаем товары из базы данных.
        """
        catalog_ids = self.cart.keys()
        # получаем товары и добавляем их в корзину
        products = Catalog.objects.filter(id__in=catalog_ids)

        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """
        Считаем сколько товаров в корзине
        """
        return sum(item['quantity'] for item in self.cart.values())

    def add(self, product, quantity=1):
        """
        Добавляем товар в корзину или обновляем его количество.
        """
        product_id = str(product.id)
        product_count = Catalog.objects.get(id=product_id).count
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0,
                                     'price': str(product.price)}
        if self.cart[product_id]['quantity'] < product_count:
            self.cart[product_id]['quantity'] += quantity
            self.save()
            return True
        else:
            return False

    def decrement(self, product, quantity=1):
        product_id = str(product.id)
        self.cart[product_id]['quantity'] -= quantity
        if self.cart[product_id]['quantity'] == 0:
            self.remove(product)
        self.save()

    def save(self):
        # сохраняем товар
        self.session.modified = True

    def remove(self, product):
        """
        Удаляем товар
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def get_total_price(self):
        # получаем общую стоимость
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())
