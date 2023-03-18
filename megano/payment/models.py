from django.db import models
from app_shop.models import User
from cart.cart import Cart


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)



