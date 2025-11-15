from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from .models import Address
from payments.models import Payment

PAYMENT_CHOICES = (
    ('S', 'Stripe'),
    ('P', 'PayPal'),
)

class CheckoutForm(forms.Form):
    
    street_address = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '1234 Main St',
            'id': 'street_address',
        })
    )
    apartment_address = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Apartment or suite',
            'id': 'apartment_address',
        })
    )
    country = CountryField(
        blank_label='(select country)').formfield(
            required=False,
            widget=CountrySelectWidget(attrs={
                'class': 'custom-select d-block w-100',
                'id': 'billing_country'
            }))
    zip = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '123456',
            'id': 'zip',
        })
    )
    address_type = forms.CharField(
        required=False,
        widget=forms.RadioSelect(attrs={
            'class': 'form-control',
            'id': 'address_type',
        })
    )
    default = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
            'id': 'default'
        })
    )
    payment_option = forms.ChoiceField(widget=forms.RadioSelect(attrs={
        'class': 'form-control',
        'id': 'payment_option'
    }), choices=PAYMENT_CHOICES)


class CouponForm(forms.Form):
    code = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter coupon code',
        'aria-label': 'Enter coupon code',
        'aria-describedby': 'basic-addon2',
    }))  