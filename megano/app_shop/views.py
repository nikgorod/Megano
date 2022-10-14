from django.shortcuts import render, redirect
from django.views import View
from .models import GoodCategory
from .registration import *


class MainPage(View):

    def get(self, request):
        good_categories = GoodCategory.objects.filter(active_goods=True)

        return render(request, 'app_shop/index.html', {'good_categories': good_categories})
