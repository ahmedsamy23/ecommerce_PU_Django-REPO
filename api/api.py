from rest_framework.response import Response
from .serializers import ItemSerializer , OrderSerializer , PaymentSerializer
from core.models import Item , Order , Payment
from rest_framework import generics


class ItemListApi(generics.ListCreateAPIView):
    
    model = Item # not necessary
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


class ItemDetailApi(generics.RetrieveUpdateDestroyAPIView):
    
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    lookup_field = 'id' # to get the item by id

class OrderListApi(generics.ListCreateAPIView):
    
    model = Order # not necessary
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class OrderDetailApi(generics.RetrieveUpdateDestroyAPIView):
    
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    lookup_field = 'id' # to get the order by id


class PaymentListApi(generics.ListCreateAPIView):
    
    model = Payment # not necessary
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

class PaymentDetailApi(generics.RetrieveUpdateDestroyAPIView):
    
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    lookup_field = 'id' # to get the payment by id
