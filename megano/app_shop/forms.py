from django.contrib.auth.forms import UserCreationForm
from .models import User
from django import forms


class UserFormRegister(forms.Form):
    """Форма пользователя при регистрации"""
    last_name = forms.CharField(label='Фамилия:',)
    first_name = forms.CharField(label='Имя:',)
    middle_name = forms.CharField(label='Отчество:',)
    tel = forms.CharField(label='Телефон:', max_length=18)
    email = forms.CharField(label='Email:', widget=forms.EmailInput())

    def __init__(self, *args, **kwargs):
        super(UserFormRegister, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class UserFormPassword(UserCreationForm):
    """Форма пользователя"""
    class Meta:
        model = User
        fields = ('password1', 'password2')
