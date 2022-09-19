class GoodAtBasket:
    """Сервис корзины с товарами"""

    def add_to_basket(self, request, good_id: int):
        """Метод по добавлению товара в корзину"""
        pass

    def remove_from_basket(self, request, good_id: int):
        """Метод по удалению товара из корзины"""
        pass

    def get_list_of_goods_at_basket(self):
        """Получение списка товаров в корзине"""
        pass


def send_notification(message: str):
    """Метод выводящий уведомление при совершении какого-либо действия"""
    pass


class AddReview:
    """Сервис по добавлению отзыва"""

    def add_review_to_good(self, text: str, user_id: int, good_id: int):
        """Метод по добавлению отзыва к товару"""
        pass


class ViewedGoods:
    """Сервис просмотренных товаров"""

    def get_list_of_viewed_goods(self):
        """Метод получения списка просмотренных товаров"""
        pass


class Payment:
    """Сервис оплаты"""

    def pay_for_order(self, order_id: int, user_id: int):
        """Метод оплаты"""
        pass


class AdminSettings:
    """Нужна подсказка"""
