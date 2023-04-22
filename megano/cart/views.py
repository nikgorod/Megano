from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.http import require_POST
from app_shop.models import Catalog, GoodCategory
from .cart import Cart
from .forms import CartAddProductForm
from app_shop.forms import SearchForm
from django.contrib import messages
from payment.views import user_params


def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Catalog, id=product_id)
    success = cart.add(product=product)
    if not success:
        messages.add_message(request, messages.INFO, 'Превышено кол-во товара в наличии...')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def decrement_item(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Catalog, id=product_id)
    cart.decrement(product=product)
    return redirect('cart_detail')


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Catalog, id=product_id)
    cart.remove(product)
    return redirect('cart_detail')


def cart_detail(request):
    cart = Cart(request)
    cart_items_num = len(cart)
    search_form = SearchForm()
    good_categories = GoodCategory.objects.prefetch_related('good').filter(active_goods=True)

    return render(request, 'cart/detail.html', {'cart': cart, 'search_form': search_form,
                                                'good_categories': good_categories,
                                                'cart_items_num': cart_items_num})
