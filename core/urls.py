from django.urls import path
from .views import (
  ItemDetailView , 
  OrderSummaryView , 
  ItemListView , 
  RequestRefundView , 
  add_quantity , 
  remove_from_cart , 
  remove_single_item_from_cart ,
  add_to_cart,
)

app_name = 'core'

urlpatterns = [
    path('', ItemListView.as_view(), name='item-list'),
    path('item-list-by-category/<str:category>', ItemListView.as_view(), name='item-list-by-category'),
    path('shop/<slug:slug>', ItemDetailView.as_view(), name='product'),
    path('add-to-cart/<slug:slug>', add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<slug:slug>', remove_from_cart, name='remove-from-cart'),
    path('remove-single-item-from-cart/<slug:slug>', remove_single_item_from_cart, name='remove-single-item-from-cart'),
    path('order-summary', OrderSummaryView.as_view(), name='order-summary'),
    path('add-quantity/<slug:slug>', add_quantity, name='add-quantity'),
    path('request-refund', RequestRefundView.as_view(), name='request-refund'),
]

