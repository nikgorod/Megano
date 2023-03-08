from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),
    path('add/<int:product_id>/',
         views.cart_add,
         name='cart_add'),
    path('decrement_item/<int:product_id>/', views.decrement_item, name='cart_decrement'),
    path('remove/<int:product_id>/',
         views.cart_remove,
         name='cart_remove'),
]