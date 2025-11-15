import django_filters
from .models import Item
from django.db.models import Q

class SearchFilter(django_filters.FilterSet):
    
    q = django_filters.CharFilter(method='filter_by_all_text', label='Search')
    

    def filter_by_all_text(self, queryset, name, value):
        if value:
            return queryset.filter(
                Q(title__icontains=value) | Q(description__icontains=value)
            )
    
    class Meta:
        model = Item
        fields = ['q']