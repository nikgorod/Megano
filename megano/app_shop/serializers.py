from rest_framework import serializers
from .models import DynamicSiteSettings


class SiteSettingsSerializer(serializers.ModelSerializer):

    class Meta:
        model = DynamicSiteSettings
        fields = ['title', 'cache_timeout', 'meta_content', 'logo']
