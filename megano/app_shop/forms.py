from django.contrib.auth.forms import UserCreationForm
from .models import User, Shop, Review, UserProfile
from django import forms


class UserFormRegister(forms.Form):
    """Форма пользователя при регистрации"""
    last_name = forms.CharField(label='Last name:', )
    first_name = forms.CharField(label='First name:', )
    middle_name = forms.CharField(label='Middle name:', required=False)
    tel = forms.CharField(label='Phone:', max_length=18)

    def __init__(self, *args, **kwargs):
        super(UserFormRegister, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class UserFormPassword(UserCreationForm):
    """Форма пользователя"""

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')


class ReviewForm(forms.ModelForm):
    """Форма для отзыва"""
    class Meta:
        model = Review
        fields = ['review', ]

    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)
        self.fields['review'].attrs = {
            'class': 'form-textarea',
            'name': 'review',
            'id': 'review',
            'placeholder': 'Review'
        }


class ProfileForm(forms.ModelForm):
    """Форма для редактирования профиля"""
    email = forms.EmailField()

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['avatar'].attrs = {
            'name': 'avatar',
            'id': 'avatar',
            'type': 'file',
            'data-validate': 'onlyImgAvatar',
        }
        self.fields['avatar'].widget.attrs['class'] = "Profile-file form-input"
        self.fields['avatar'].required = False
        self.fields['last_name'].attrs = {
            'id': 'name',
            'name': 'name',
            'type': 'text',
            'value': f'{self.initial.get("last_name")}'
        }
        self.fields['last_name'].widget.attrs['class'] = "form-input"

        self.fields['tel'].attrs = {
            'id': 'phone',
            'name': 'phone',
            'type': 'text',
            'value': f'{self.initial.get("tel")}'
        }
        self.fields['tel'].widget.attrs['class'] = "form-input mask-phone"
        self.fields['email'].widget.attrs = {
            'class': 'form-input',
            'id': 'mail',
            'name': 'mail',
            'type': 'text',
            'value': f'{self.initial.get("email")}'
        }

    class Meta:
        model = UserProfile
        fields = ['avatar', 'last_name', 'tel', ]


class FilterForm(forms.Form):
    """Форма для фильтрации каталога"""
    def __init__(self, *args, category_id=None, **kwargs):
        super(FilterForm, self).__init__(*args, **kwargs)
        self.category_id = category_id
        self.fields['price'] = forms.CharField(widget=forms.TextInput(attrs={'class': 'range-line',
                                                          'id': 'price',
                                                          'data-type': 'double',
                                                          'data-min': '7',
                                                          'data-max': '300',
                                                          'data-from': '10',
                                                          'data-to': '100'
                                                          }))

        self.fields['name'] = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input form-input_full',
                                                         'id': 'title',
                                                         'placeholder': 'Название',
                                                         }), required=False)
        self.fields['existence'] = forms.BooleanField(required=False)
        self.fields['delivery'] = forms.BooleanField(required=False)

        CHOICES = [(i_shop.name, i_shop.name) for i_shop in Shop.objects.all().defer('description')]

        self.fields['shops'] = forms.MultipleChoiceField(choices=CHOICES,
                                          widget=forms.CheckboxSelectMultiple, required=False)

        # specification_choices = [(i_specification.specification.specification,
        #                           [value.value for value in GoodSpecification.objects.all().filter(specification_id=i_specification.id)])
        #                          for i_specification in GoodSpecification.objects.all().filter(
        #     specification__category_id=self.category_id
        # )]
        #
        # self.fields['specifications'] = forms.MultipleChoiceField(choices=specification_choices,
        #                                   widget=forms.CheckboxSelectMultiple, required=False)
        #
        # print(specification_choices)


class SearchForm(forms.Form):
    """Форма для поиска по сайту"""
    search = forms.CharField(widget=forms.TextInput(attrs={'class': 'search-input',
                                                          'id': 'query',
                                                            'name': 'query',
                                                           'placeholder': 'What are you looking for ...'
                                                          }), label='', required=False)
