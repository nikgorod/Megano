from django.contrib import admin
from django.db.utils import ProgrammingError

from .models import GoodCategory, UserProfile, Shop, User, Good, GoodTags, Catalog, CatalogImages, DynamicSiteSettings
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin


@admin.register(GoodCategory)
class GoodCategoryAdmin(admin.ModelAdmin):
    """Админ модель для категорий товара"""
    model = GoodCategory
    list_display = ['name']
    search_fields = ['name']
    list_filter = ['name', 'active_goods']


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """Админ модель для роли пользователя на сайте"""
    model = UserProfile
    list_display = ['user', 'first_name', 'last_name', 'tel']
    search_fields = ['first_name', 'tel', 'last_name']


@admin.register(User)
class UserAdmin(DjangoUserAdmin):

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    """Админ модель для роли магазина"""
    model = Shop
    list_display = ['name']
    search_fields = ['name']


@admin.register(Good)
class GoodAdmin(admin.ModelAdmin):
    """Админ модель товара"""
    model = Good
    list_display = ['name', 'category']
    search_fields = ['name', 'category', 'description']


class CatalogImagesInLine(admin.TabularInline):
    model = CatalogImages
    extra = 0


@admin.register(Catalog)
class CatalogAdmin(admin.ModelAdmin):
    """Админ модель каталога"""
    model = Catalog
    list_display = ['good', 'shop', 'count']
    list_filter = ['count', 'discount', 'shop']
    inlines = [CatalogImagesInLine]


@admin.register(CatalogImages)
class CatalogImagesAdmin(admin.ModelAdmin):
    """Админ модель изображений каталога"""
    model = CatalogImages
    list_display = ['catalog']


@admin.register(GoodTags)
class GoodTagsAdmin(admin.ModelAdmin):
    """Админ модель тегов"""
    model = GoodTags
    list_display = ['name']


@admin.register(DynamicSiteSettings)
class DynamicSiteSettingsAdmin(admin.ModelAdmin):

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)

        try:
            DynamicSiteSettings.load().save()

        except ProgrammingError:
            pass

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

