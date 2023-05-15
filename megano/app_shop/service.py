from app_shop.models import Review, UserProfile


def ordering_catalog(ordering):
    """Метод сортировки"""
    try:
        if ordering.startswith('-'):
            if ordering[1:] == 'price':
                return '-price'
            elif ordering[1:] == 'reviews':
                return '-reviews_num'
            elif ordering[1:] == 'release_year':
                return '-good__release_year'
            elif ordering[1:] == 'purchases_number':
                return '-purchases_number'
        else:
            if ordering == 'price':
                return 'price'
            elif ordering == 'reviews':
                return 'reviews_num'
            elif ordering == 'release_year':
                return 'good__release_year'
            elif ordering == 'purchases_number':
                return 'purchases_number'
    except AttributeError:
        return None


class GoodAtBasket:
    """Сервис корзины с товарами"""

    def add_to_basket(self, request, good_id: int):
        """Метод по добавлению товара в корзину"""
        pass

    def remove_from_basket(self, request, good_id: int):
        """Метод по удалению товара из корзины"""
        pass

    def change_num_of_goods_in_basket(self, request):
        """Метод по изменению кол-ва товара в корзине"""
        pass

    def get_list_of_goods_at_basket(self):
        """Получение списка товаров в корзине"""
        pass

    def get_num_of_goods_in_basket(self, request):
        """Метод получения кол-ва товара в корзине"""
        pass


def send_notification(message: str):
    """Метод выводящий уведомление при совершении какого-либо действия"""
    pass


class AddReview:
    """Сервис по добавлению отзыва"""
    @staticmethod
    def add_review_to_good(form, request, pk):
        new_review = form.save(commit=False)
        new_review.catalog_id = pk
        new_review.profile_id = request.user.profile.id
        new_review.save()

    @staticmethod
    def get_list_of_reviews_at_good(catalog_id):
        reviews = Review.objects.filter(catalog_id=catalog_id)
        return reviews

    def get_num_of_reviews_at_good(self, request):
        """Метод получения кол-ва отзывов о товаре"""
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

    def get_status_of_payment(self):
        """Метод получения статуса оплаты"""
        pass


class ProfileEdit:
    """Сервис по редактированию пользователя"""
    @staticmethod
    def username_edit(profile, new_name):
        if len(new_name) == 3:
            profile.last_name = new_name[0]
            profile.first_name = new_name[1]
            profile.middle_name = new_name[2]
            return True
        else:
            return False

    @staticmethod
    def avatar_edit(profile, new_avatar):
        profile.avatar = new_avatar

    @staticmethod
    def tel_edit(profile, new_tel):
        old_tel = profile.tel
        if new_tel != old_tel:
            is_tel_exist = UserProfile.objects.filter(tel=new_tel)
            if not is_tel_exist:
                profile.tel = new_tel
                return True
            else:
                return False
        else:
            return True

    @staticmethod
    def email_edit(profile, new_email):
        old_email = profile.user.email
        if new_email != old_email:
            is_email_exist = UserProfile.objects.filter(user__email=new_email)
            if not is_email_exist:
                profile.user.email = new_email
                return True
            else:
                return False
        else:
            return True
