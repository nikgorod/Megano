from django.urls import path
from .views import MainPage, register_view, ShopLoginView, ShopLogoutView, ShopPasswordReset, ShopPasswordResetDone, \
    ShopPasswordResetConfirm, ShopPasswordResetComplete, SettingsApiView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('shop/main_page/', MainPage.as_view(), name='main_page'),
    path('shop/register/', register_view, name='register'),
    path('shop/login/', ShopLoginView.as_view(), name='login'),
    path('shop/logout/', ShopLogoutView.as_view(), name='logout'),
    path('shop/reset_password/', ShopPasswordReset.as_view(), name='reset_password'),
    path('shop/reset_password/done/', ShopPasswordResetDone.as_view(), name='password_reset_done'),
    path('shop/reset/<uidb64>/<token>/', ShopPasswordResetConfirm.as_view(), name='password_reset_confirm'),
    path('shop/reset/complete/', ShopPasswordResetComplete.as_view(), name='password_reset_complete'),
    path('shop/settings_api/', SettingsApiView.as_view(), name='settings_api')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
