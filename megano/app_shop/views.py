from django.shortcuts import render, redirect
from django.views import View
from rest_framework.views import APIView
from .serializers import SiteSettingsSerializer
from .models import GoodCategory, DynamicSiteSettings
from .registration import *
from rest_framework.response import Response


class SettingsApiView(APIView):

    def get(self, request):
        settings = DynamicSiteSettings.objects.get()
        serializer = SiteSettingsSerializer(settings)
        return Response(serializer.data)


def site_settings(request):
    return {'site_settings': DynamicSiteSettings.load()}


class MainPage(View):

    def get(self, request):
        good_categories = GoodCategory.objects.filter(active_goods=True)

        return render(request, 'app_shop/index.html', {'good_categories': good_categories})
