from django import forms
from .models import Payment


class PaymentParamsForm(forms.Form):
    """Форма оплаты заказа"""

    CHOICES_DELIVERY = [('1', 'Обычная доставка'), ('2', 'Экспресс доставка')]
    delivery = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES_DELIVERY, required=True)
    city = forms.CharField(max_length=30, label='Город:', required=True)
    address = forms.CharField(max_length=100, label='Адрес:', required=True)
    CHOICES_CARD = [('1', 'Онлайн картой'), ('2', 'Онлайн со случайного чужого счета')]
    card = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES_CARD, required=True)


class PaymentForm(forms.ModelForm):

    class Meta:
        model = Payment
        fields = ('card_num', )

    def __init__(self, *args, **kwargs):
        super(PaymentForm, self).__init__(*args, **kwargs)
        self.fields['card_num'].widget.attrs['class'] = 'form-input Payment-bill'
        self.fields['card_num'].widget.attrs['placeholder'] = '9999 9999'
        self.fields['card_num'].widget.attrs['data-mask'] = '9999 9999'

