from django.urls import path
from .views import ItemListView

app_name = 'shop'

urlpatterns = [
    path('', ItemListView.as_view(), name='shop'),
]