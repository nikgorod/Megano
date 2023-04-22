from celery.result import AsyncResult
from django.db import transaction
from django.shortcuts import render, redirect
from app_shop.forms import SearchForm, UserFormRegister, UserFormPassword
from app_shop.models import DynamicSiteSettings
from cart.cart import Cart
from .forms import PaymentParamsForm, PaymentForm
from .models import Delivery, Payment, Order, OrdersToGoods
from django.contrib import messages
from .tasks import confirm_payment
from app_shop.models import Catalog


def get_delivery_price(total_cost, delivery_type):
    order_cost = DynamicSiteSettings.objects.first().order_cost
    delivery_cost = DynamicSiteSettings.objects.first().delivery_cost
    express_delivery_cost = DynamicSiteSettings.objects.first().express_delivery_cost
    if delivery_type == '1':
        if total_cost > order_cost:
            return 0
        else:
            return delivery_cost
    else:
        if total_cost > order_cost:
            return express_delivery_cost
        else:
            return delivery_cost + express_delivery_cost


def user_params(request):
    cart = Cart(request)
    search_form = SearchForm()
    if request.method == 'POST':
        payment_form = PaymentParamsForm(request.POST)
        if payment_form.is_valid():
            user = request.user
            total_cost = cart.get_total_price()
            delivery_type = payment_form.cleaned_data['delivery']
            delivery_cost = get_delivery_price(total_cost, delivery_type)
            with transaction.atomic():
                delivery = Delivery.objects.create(delivery_type=payment_form.cleaned_data['delivery'],
                                                   city=payment_form.cleaned_data['city'],
                                                   address=payment_form.cleaned_data['address'],
                                                   delivery_cost=delivery_cost)
                payment = Payment.objects.create(code='Не оплачено', payment_type=payment_form.cleaned_data['card'])
                order = Order.objects.create(user=user, amount=total_cost, delivery=delivery, payment=payment)
                flag = True
                for i_item in cart:
                    OrdersToGoods.objects.create(order=order, good=i_item['product'], quantity=i_item['quantity'])
                    catalog = Catalog.objects.get(id=i_item['product'].id)
                    if catalog.count < i_item['quantity']:
                        flag = False
                        messages.add_message(request, messages.INFO, 'Превышено допустимое кол-во товара!')
                        break
                if flag:
                    return redirect('payment', order_id=order.id, payment_type=payment_form.cleaned_data['card'])
    payment_form = PaymentParamsForm()
    user_form = UserFormRegister()
    user_form_password = UserFormPassword()
    return render(request, 'payment/user_params.html', {'search_form': search_form,
                                                        'payment_form': payment_form,
                                                        'cart': cart,
                                                        'user_form': user_form,
                                                        'user_form_password': user_form_password})


# celery -A megano worker -l INFO -P solo
def payment(request, order_id, payment_type):
    search_form = SearchForm()
    if request.method == 'POST':
        payment_form = PaymentForm(request.POST)
        if payment_form.is_valid():
            card_num = payment_form.cleaned_data['card_num'].replace(' ', '')
            print(card_num)
            if len(card_num) == 8:
                task = confirm_payment.apply_async((card_num, request.user.pk), countdown=5)
                return redirect('payment_confirm', task_id=task.task_id, order_id=order_id, card_num=card_num)
            else:
                messages.add_message(request, messages.INFO, 'Номер карты должен состоять из восьми цифр!')
    payment_form = PaymentForm()
    if payment_type == '1':
        return render(request, 'payment/payment.html', {
            'search_form': search_form,
            'payment_form': payment_form
        })
    return render(request, 'payment/random_payment.html', {
        'search_form': search_form,
        'payment_form': payment_form
    })


def repayment(request, order_id):
    payment_form = PaymentParamsForm()
    if request.method == 'POST':
        payment_form = PaymentParamsForm(request.POST)
        if payment_form.is_valid():
            order = Order.objects.get(id=order_id)
            order.delivery.delivery_type = payment_form.cleaned_data['delivery']
            order.delivery.city = payment_form.cleaned_data['city']
            order.delivery.address = payment_form.cleaned_data['address']
            order.delivery.delivery_cost = get_delivery_price(order.amount, payment_form.cleaned_data['delivery'])
            order.payment.payment_type = payment_form.cleaned_data['card']
            order.delivery.save()
            order.payment.save()
            order.save()
            return redirect('payment', order_id=order.id, payment_type=payment_form.cleaned_data['card'])
    search_form = SearchForm()
    return render(request, 'payment/repayment_params.html', {'search_form': search_form,
                                                             'payment_form': payment_form, })


def payment_confirm(request, order_id, task_id, card_num):
    result = AsyncResult(task_id).get()
    cart = Cart(request)
    if result == 1:
        order = Order.objects.get(id=order_id)
        payment = Payment.objects.get(id=order.payment.pk)
        payment.code = 'Оплачено'
        payment.card_num = card_num
        payment.save()
        for i_item in cart:
            catalog = Catalog.objects.get(id=i_item['product'].id)
            catalog.purchases_number += i_item['quantity']
            catalog.count -= i_item['quantity']
            catalog.save()
            cart.remove(i_item['product'])
    return redirect('personal', pk=request.user.pk)
