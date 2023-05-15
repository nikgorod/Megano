from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import (CatalogAllListView, CatalogDetailView, CatalogListView,
                    MainPage, OrderDetailView, OrdersDetailView,
                    PersonalDetailView, ProfileDetailView, SettingsApiView,
                    ShopLoginView, ShopLogoutView, ShopPasswordReset,
                    ShopPasswordResetComplete, ShopPasswordResetConfirm,
                    ShopPasswordResetDone, register_view)

urlpatterns = [
    # Main
    path('shop/main_page/', MainPage.as_view(), name='main_page'),
    path('shop/settings_api/', SettingsApiView.as_view(), name='settings_api'),

    # Registration
    path('shop/register/', register_view, name='register'),
    path('shop/login/', ShopLoginView.as_view(), name='login'),
    path('shop/logout/', ShopLogoutView.as_view(), name='logout'),
    path('shop/reset_password/', ShopPasswordReset.as_view(), name='reset_password'),
    path('shop/reset_password/done/', ShopPasswordResetDone.as_view(), name='password_reset_done'),
    path('shop/reset/<uidb64>/<token>/', ShopPasswordResetConfirm.as_view(), name='password_reset_confirm'),
    path('shop/reset/complete/', ShopPasswordResetComplete.as_view(), name='password_reset_complete'),

    # Catalog
    path('shop/catalog/', CatalogAllListView.as_view(), name='catalog_all'),
    path('shop/catalog/<int:category_id>/', CatalogListView.as_view(), name='catalog'),
    path('shop/catalog/detail/<int:pk>/', CatalogDetailView.as_view(), name='catalog_detail'),

    # Profile
    path('shop/user/<int:pk>/', PersonalDetailView.as_view(), name='personal'),
    path('shop/user/profile/<int:pk>/', ProfileDetailView.as_view(), name='profile'),
    path('shop/user/orders/<int:pk>/', OrdersDetailView.as_view(), name='orders'),
    path('shop/user/<int:pk>/order/<int:order_id>/', OrderDetailView.as_view(), name='order')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
