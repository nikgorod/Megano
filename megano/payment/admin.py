from django.contrib import admin

from .models import Order, OrdersToGoods


class OrderGoodsInline(admin.TabularInline):
    model = OrdersToGoods
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    model = Order
    list_display = ['user', 'date', 'amount']
    inlines = [OrderGoodsInline]
