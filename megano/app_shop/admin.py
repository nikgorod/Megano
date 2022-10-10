from django.contrib import admin
from .models import GoodCategory, UserProfile, Shop


class GoodCategoryAdmin(admin.ModelAdmin):
    """Админ модель для категорий товара"""
    model = GoodCategory
    list_display = ['name']
    search_fields = ['name']
    list_filter = ['name', 'active_goods']


class UserProfileAdmin(admin.ModelAdmin):
    """Админ модель для роли пользователя на сайте"""
    model = UserProfile
    list_display = ['first_name', 'last_name', 'email']
    search_fields = ['first_name', 'email', 'tel']
    list_filter = ['balance']


class ShopAdmin(admin.ModelAdmin):
    """Админ модель для роли магазина"""
    model = Shop
    list_display = ['name']
    search_fields = ['name']


admin.site.register(GoodCategory, GoodCategoryAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Shop, ShopAdmin)
