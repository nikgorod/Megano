from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User
from django import forms


class UserFormRegister(forms.Form):
    """Форма пользователя при регистрации"""
    last_name = forms.CharField(label='Last name:',)
    first_name = forms.CharField(label='First name:',)
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

