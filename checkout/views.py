from django.shortcuts import render
from .forms import CheckoutForm , CouponForm
from django.views.generic import View 
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Address
from core.models import Coupon, Order
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.urls import reverse
from django.db.models import ObjectDoesNotExist
from payments.models import Payment

# Create your views here.


class CheckoutView(View):

    def get(self , *args , **kwargs):
        try:
            order = Order.objects.get(user = self.request.user , ordered = False)
            if order.get_total() <= 0:
                messages.error(self.request , "Your cart is empty")
                return redirect("core:item-list")
            context = {
                'order': order,
                'form': CheckoutForm(),
                'coupon_form': CouponForm(),
                'DISPLAY_COUPON_FORM': True,
            }
            return render(self.request , 'checkout/checkout.html' , context)
        except ObjectDoesNotExist:
            messages.warning(self.request , "You do not have an active order")
            return redirect("checkout:checkout")

    def post(self , *args , **kwargs):
        
        form = CheckoutForm(self.request.POST or None)
        try : 
            order = Order.objects.get(user = self.request.user , ordered = False)
            if form.is_valid():
                street_address = form.cleaned_data.get('street_address')
                apartment_address = form.cleaned_data.get('apartment_address')
                country = form.cleaned_data.get('country')
                zip = form.cleaned_data.get('zip')
                #address_type = form.cleaned_data.get('address_type')
                shipping_address = Address(
                    user = self.request.user,
                    street_address = street_address,
                    apartment_address = apartment_address,
                    country = country,
                    zip = zip,
                )
                shipping_address.save()
                order.shipping_address = shipping_address
                order.save()
            else:
                messages.warning(self.request , "Please fill in required shipping address fields")
                return redirect("checkout:checkout")
            
            payment_option = form.cleaned_data.get('payment_option')
            if payment_option == 'P':
                return redirect('payments:payment' , payment_option = payment_option)
            elif payment_option == 'S':
                return redirect('payments:payment' , payment_option = payment_option)
            else:
                messages.warning(self.request , "Invalid payment option")
                return redirect("checkout:checkout")
        except ObjectDoesNotExist:
            messages.warning(self.request , "You do not have an active order")
            return redirect("checkout:checkout")


def get_coupon(request , code):
    # try to get the coupon from the database if it exists
    try:
        coupon = Coupon.objects.get(code = code)
        return coupon
    except ObjectDoesNotExist:
        return None

class AddCouponView(View):
    def post(self , *args , **kwargs):
        form = CouponForm(self.request.POST or None)
        if form.is_valid():
            try:
                code = form.cleaned_data.get('code')
                order = Order.objects.get(user = self.request.user , ordered = False)
                coupon = get_coupon(self.request , code)
                if coupon is None :
                    messages.warning(self.request , "Invalid coupon code")
                    return redirect("checkout:checkout")
                order.coupon = coupon
                order.save()
                messages.success(self.request , "Coupon applied successfully")
                return redirect("checkout:checkout")
            except ObjectDoesNotExist:
                messages.warning(self.request , "You do not have an active order")
                return redirect("checkout:checkout")
        else:
            messages.warning(self.request , "Invalid coupon code")
            return redirect("checkout:checkout")
                