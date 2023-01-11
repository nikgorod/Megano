from .models import Catalog
import django_filters
from django import forms
from .models import Shop, GoodSpecification, Manufacturer


def price_filter(queryset, price, value):
    """Фильтр по цене"""
    return queryset.filter(price__range=map(int, value.split(';')))


def count_filter(queryset, count, value):
    """Фильтр по наличию товара"""
    return queryset.filter(count__gt=0)


class CatalogFilter(django_filters.FilterSet):
    """Фильтр для каталога"""
    CHOICES = [(i_shop.name, i_shop.name) for i_shop in Shop.objects.all().defer('description')]
    CHOICES_MANUFACTURER = [(i_good.id, i_good.name)
                            for i_good in Manufacturer.objects.filter(category_id=1)]
    good_specification_choices = [(spec, spec.value) for spec in GoodSpecification.objects.filter(good__category_id=1)]

    specification_choices = [(i_specification.id, i_specification)
                             for i_specification in GoodSpecification.objects.filter(specification__category_id=1)]
    price = django_filters.CharFilter(field_name='price', method=price_filter, widget=forms.TextInput(attrs={
        'class': 'range-line',
        'id': 'price',
        'data-type': 'double',
        'data-min': '7',
        'data-max': '5000',
        'data-from': '50',
        'data-to': '1000'
    }))

    good__name = django_filters.CharFilter(lookup_expr='icontains', widget=forms.TextInput(attrs={
        'class': 'form-input form-input_full',
        'id': 'title',
        'placeholder': 'Название',
    }))

    good__manufacturer = django_filters.MultipleChoiceFilter(choices=CHOICES_MANUFACTURER,
                                                             widget=forms.CheckboxSelectMultiple())

    count = django_filters.CharFilter(field_name='count', method=count_filter, widget=forms.CheckboxInput())

    shop__name = django_filters.MultipleChoiceFilter(choices=CHOICES, widget=forms.CheckboxSelectMultiple())

    # Не получается реализовать
    good__good_specifications = django_filters.MultipleChoiceFilter(choices=specification_choices,
                                                                    widget=forms.CheckboxSelectMultiple())

    class Meta:
        model = Catalog
        fields = ['price', 'shop__name', 'good__name', 'count', 'good__good_specifications', 'good__manufacturer']
