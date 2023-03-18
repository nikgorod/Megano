from django import forms


class CartAddProductForm(forms.Form):
    quantity = forms.IntegerField(widget=forms.NumberInput)

    def __init__(self, *args, **kwargs):
        super(CartAddProductForm, self).__init__(*args, **kwargs)
        self.fields['quantity'].widget.attrs['class'] = 'Amount-input form-input'
        self.fields['quantity'].widget.attrs['value'] = 1