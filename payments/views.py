from django.shortcuts import render, redirect
from django.db.models import ObjectDoesNotExist
from django.db import transaction
from .models import Payment
import stripe
from django.conf import settings
from django.views.generic import View
from .forms import PaymentForm
from django.contrib import messages
from core.models import Order
import logging
import string
import random

stripe.api_key = settings.STRIPE_SECRET_KEY

# Create your views here.

PAYMENT_METHODS = (
    ('S', 'Stripe'),
    ('P', 'PayPal'),
)

def create_ref_code():
    """Generate a random reference code for orders"""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=20))


class PaymentView(View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect('core:item-list')
            
        if order.shipping_address:
            context = {
                'order': order,
                'DISPLAY_COUPON_FORM': False,
                'form': PaymentForm(),
                'stripe_public_key': settings.STRIPE_PUBLISHABLE_KEY,
            }
            
            try:
                userprofile = self.request.user.userprofile
                if userprofile.stripe_customer_id:
                    cards = stripe.Customer.list_sources(
                        userprofile.stripe_customer_id,
                        limit=3,
                        object='card'
                    )
                    card_list = cards['data']
                    if len(card_list) > 0:
                        context.update({
                            'card': card_list[0]
                        })
            except Exception as e:
                logging.error(f"Error fetching card data: {str(e)}")
                # Continue without card data
                
            return render(self.request, 'payments/payment.html', context)
        else:
            messages.warning(self.request, "You need to add a shipping address")
            return redirect('checkout:checkout')
    
    def post(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect('core:item-list')
            
        form = PaymentForm(self.request.POST)
        userprofile = self.request.user.userprofile
        
        if form.is_valid():
            save = form.cleaned_data.get('save')
            use_default = form.cleaned_data.get('use_default')
            token = self.request.POST.get('stripeToken')
            
            if save:
                if not userprofile.stripe_customer_id:
                    try:
                        customer = stripe.Customer.create(
                            email=self.request.user.email,
                            source=token
                        )
                        userprofile.stripe_customer_id = customer.id
                        userprofile.one_click_purchasing = True
                        userprofile.save()
                    except Exception as e:
                        logging.error(f"Error creating Stripe customer: {str(e)}")
                        messages.warning(self.request, "Error saving card information")
                else:
                    try:
                        stripe.Customer.create_source(
                            userprofile.stripe_customer_id,
                            source=token
                        )
                    except Exception as e:
                        logging.error(f"Error adding card to customer: {str(e)}")

            amount = int(order.get_total() * 100)

            try:
                # Use Stripe's library to make requests
                if use_default:
                    if not userprofile.stripe_customer_id:
                        messages.warning(self.request, "No default payment method found")
                        return redirect('payments:payment', payment_option='stripe')
                        
                    charge = stripe.Charge.create(
                        amount=amount,  # convert to cents
                        currency='usd',
                        customer=userprofile.stripe_customer_id,
                        description='Charge for order'
                    )
                else:
                    if not token:
                        messages.warning(self.request, "No payment token provided")
                        return redirect('payments:payment', payment_option='stripe')
                        
                    charge = stripe.Charge.create(
                        amount=amount,  # convert to cents
                        currency='usd',
                        source=token,
                        description='Charge for order'
                    )

                with transaction.atomic():
                    # create the payment
                    payment = Payment()
                    payment.stripe_charge_id = charge['id']
                    payment.user = self.request.user
                    payment.amount = order.get_total()
                    payment.payment_method = 'S'
                    payment.save()

                    # assign the payment to the order
                    order_items = order.items.all()
                    order_items.update(ordered=True)
                    for item in order_items:
                        item.save()

                    # update the order
                    order.ordered = True
                    order.payment = payment
                    order.ref_code = create_ref_code()
                    order.save()

                messages.success(self.request, "Your order was successful!")
                return redirect('core:item-list')
            
            except stripe.error.CardError as e:
                # Since it's a decline, stripe.error.CardError will be caught
                body = e.json_body
                err = body.get('error', {})
                messages.warning(self.request, f"Card Error: {err.get('message', 'Your card was declined')}")
                return redirect('payments:payment', payment_option='stripe')
                
            except stripe.error.RateLimitError as e:
                # Too many requests made to the API too quickly
                messages.warning(self.request, "Rate limit error. Please try again in a moment.")
                return redirect('payments:payment', payment_option='stripe')
                
            except stripe.error.InvalidRequestError as e:
                # Invalid parameters were supplied to Stripe's API
                messages.warning(self.request, "Invalid payment parameters. Please check your information.")
                return redirect('payments:payment', payment_option='stripe')
                
            except stripe.error.AuthenticationError as e:
                # Authentication with Stripe's API failed
                messages.warning(self.request, "Authentication error. Please contact support.")
                return redirect('payments:payment', payment_option='stripe')
                
            except stripe.error.APIConnectionError as e:
                # Network communication with Stripe failed
                messages.warning(self.request, "Network error. Please check your connection and try again.")
                return redirect('payments:payment', payment_option='stripe')
                
            except stripe.error.StripeError as e:
                # Display a very generic error to the user
                messages.warning(self.request, "Something went wrong. You were not charged. Please try again.")
                return redirect('payments:payment', payment_option='stripe')
                
            except Exception as e:
                # Something else happened, completely unrelated to Stripe
                logging.error(f"Payment error: {str(e)}")
                messages.warning(self.request, "A serious error occurred. We have been notified.")
                return redirect('payments:payment', payment_option='stripe')
        else:
            messages.warning(self.request, "Please correct the form errors")
            return redirect('payments:payment', payment_option='stripe')