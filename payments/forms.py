from django import forms
from django.forms import widgets
from .models import Payment

PAYMENT_CHOICES = (
    ('S', 'Stripe'),
    ('P', 'PayPal'),
)

class PaymentForm(forms.Form):
    
    stripeToken = forms.CharField(
        required=False,
        widget=forms.HiddenInput(attrs={'id': 'stripeToken'})
    )
    
    save = forms.BooleanField(
        required=False,
        label="Save this card for future purchases",
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input', 
            'help_text': 'Save this card for future purchases',
            'id': 'save_card'
        }),
    )
    
    use_default = forms.BooleanField(
        required=False,
        label="Use default payment method",
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input', 
            'help_text': 'Use default payment method',
            'id': 'use_default_card'
        }),
    )

    def clean(self):
        cleaned_data = super().clean()
        use_default = cleaned_data.get('use_default')
        stripe_token = cleaned_data.get('stripeToken')
        
        # If not using default payment and no stripe token, it's invalid
        if not use_default and not stripe_token:
            raise forms.ValidationError(
                "Please provide payment information or select a saved payment method."
            )
        
        return cleaned_data