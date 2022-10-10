from django.urls import path
from .views import MainPage, register_view
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('shop/main_page/', MainPage.as_view(), name='main_page'),
    path('shop/register/', register_view, name='register'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
