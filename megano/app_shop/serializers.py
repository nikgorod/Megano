from rest_framework import serializers

from app_shop.models import DynamicSiteSettings


class SiteSettingsSerializer(serializers.ModelSerializer):

    class Meta:
        model = DynamicSiteSettings
        fields = ['title', 'cache_timeout', 'meta_content', 'logo']
