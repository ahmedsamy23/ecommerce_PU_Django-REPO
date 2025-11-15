from dataclasses import fields
from email import message
from django import forms
from .models import OrderItem , Refund


class QuantityForm(forms.Form):

    quantity = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control' ,
                'min': 1 ,
                'value': 1
            }
        ),
        min_value=1
    )

class RefundForm(forms.Form):

    ref_code = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control' ,
        'placeholder': 'Enter Refund Code'
    }))
    message = forms.CharField(widget=forms.Textarea(attrs={
        'rows': 4,
        'class': 'form-control' ,
        'placeholder': 'Enter Refund Reason'
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control' ,
        'placeholder': 'Enter Refund Email'
    }))
    