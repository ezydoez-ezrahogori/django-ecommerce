from django import forms
from .models import BillingAddress


class BillingAddressForm(forms.ModelForm):
    class Meta:
        model = BillingAddress
        fields = ['full_name', 'address', 'mobile',
                  'zip_code', 'city', 'country']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
