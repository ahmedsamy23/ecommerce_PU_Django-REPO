from django.urls import path
from .views import CheckoutView , AddCouponView

app_name = 'checkout'

urlpatterns = [
    path('' , CheckoutView.as_view() , name='checkout'),
    path('add-coupon' , AddCouponView.as_view() , name='add-coupon')
]