from django.urls import path
from . import api

app_name = 'api'

urlpatterns = [
    path('item-list/' , api.ItemListApi.as_view() , name = 'item-list'),
    path('item-detail/<int:id>/' , api.ItemDetailApi.as_view() , name = 'item-detail'),
    path('order-list/' , api.OrderListApi.as_view() , name = 'order-list'),
    path('order-detail/<int:id>/' , api.OrderDetailApi.as_view() , name = 'order-detail'),
    path('payment-list/' , api.PaymentListApi.as_view() , name = 'payment-list'),
    path('payment-detail/<int:id>/' , api.PaymentDetailApi.as_view() , name = 'payment-detail'),
]
