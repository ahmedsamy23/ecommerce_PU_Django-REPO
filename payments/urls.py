from django.urls import path
from . import views

app_name = 'payments'
urlpatterns = [
    path('<payment_option>' , views.PaymentView.as_view() , name='payment'),
]