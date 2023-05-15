from django.urls import path

from .views import *

urlpatterns = [
    path('user_param/', user_params, name='user_param_order'),
    path('payment/<int:order_id>/<str:payment_type>/', payment, name='payment'),
    path('payment_confirm/<int:order_id>/<str:task_id>/<str:card_num>/', payment_confirm, name='payment_confirm'),
    path('repayment/<int:order_id>/', repayment, name='repay')

]
