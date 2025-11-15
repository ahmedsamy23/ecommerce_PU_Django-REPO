from typing import override
from core.models import Item
from django.urls import reverse
from .filters import CategoryFilter
from django.views.generic import ListView
#  Create your views here.




class CategoryListView(ListView):
    model = Item
    template_name = 'categories/category_list.html'
    context_object_name = 'items'
    paginate_by = 12
    
    
    def get_queryset(self):
        queryset = super().get_queryset()

        category = self.kwargs.get('category')
        hyper_category = self.request.GET.get('hyper_category')

        if category:
            queryset = queryset.filter(category=category)
        if hyper_category:
            queryset = queryset.filter(hyper_category=hyper_category)

        self.FilterSet = CategoryFilter(self.request.GET, queryset=queryset)
        return self.FilterSet.qs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.FilterSet
        context['categories'] = Item.objects.values_list('category', flat=True).distinct()
        context['labels'] = Item.objects.values_list('label', flat=True).distinct()
        context['hyper_categories'] = Item.objects.values_list('hyper_category', flat=True).distinct()
        context['category'] = self.kwargs.get('category')
        return context
