from typing import override
from django.shortcuts import render
from django.views.generic import ListView
from core.models import Item 
from .filters import ItemFilter

# Create your views here.

class ItemListView(ListView):
    model = Item
    template_name = 'shop/shop.html'
    context_object_name = 'items'
    paginate_by = 12
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.FilterSet
        context['categories'] = Item.objects.values_list('category', flat=True).distinct()
        context['labels'] = Item.objects.values_list('label', flat=True).distinct()
        context['hyper_categories'] = Item.objects.values_list('hyper_category', flat=True).distinct()
        return context

    
    def get_queryset(self):
        queryset = super().get_queryset()
        self.FilterSet = ItemFilter(self.request.GET, queryset=queryset)
        return self.FilterSet.qs