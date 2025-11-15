import django_filters
from django import forms
from core.models import Item
from django.db.models import Q

CATEGORY_CHOICES = (
    ('Men', 'Men'),
    ('Women', 'Women'),
    ('Kids', 'Kids'),
    ('Accessories', 'Accessories'),
    ('Beauty', 'Beauty'),
)

HYPER_CATEGORY_CHOICES = (
    ('J', 'Jeans'),
    ('S', 'Shirts'),
    ('C', 'Coats'),
    ('JA', 'Jackets'),
    ('D', 'Dresses'),
    ('B', 'Bags'),
)

LABEL_CHOICES = (
    ('N', 'New'),
    ('S', 'Sale'),
    ('O','Out of Stock'),
)

class ItemFilter(django_filters.FilterSet):
    
    # Search
    q = django_filters.CharFilter(method='filter_by_all_text', label='Search')
    
    # Sorting
    sort_by = django_filters.ChoiceFilter(
        choices=[
            ('price_low', 'Price: Low to High'),
            ('price_high', 'Price: High to Low'),
            ('newest', 'Newest'),
            ('oldest', 'Oldest'),
            ('name_asc', 'Name: A to Z'),
            ('name_desc', 'Name: Z to A'),
            ('rating_asc', 'Rating: Low to High'),
            ('rating_desc', 'Rating: High to Low'),
            ('discount_asc', 'Discount: Low to High'),
        ],
        empty_label="Sort by"
    )
    # Filters
    category = django_filters.ChoiceFilter(
        choices=CATEGORY_CHOICES,
        empty_label="All Categories"
    )
    hyper_category = django_filters.ChoiceFilter(
        choices=HYPER_CATEGORY_CHOICES,
        empty_label="All Hyper Categories"
    )

    # Price range filters
    price_min = django_filters.NumberFilter(
        field_name='price',
        lookup_expr='gte',
        widget=forms.NumberInput(attrs={
            'placeholder': 'Min Price',
            'class': 'form-control'
        })
    )
    
    price_max = django_filters.NumberFilter(
        field_name='price',
        lookup_expr='lte',
        widget=forms.NumberInput(attrs={
            'placeholder': 'Max Price',
            'class': 'form-control'
        })
    )

    
    def filter_by_all_text(self, queryset, name, value):
        if value:
            return queryset.filter(
                Q(title__icontains=value) | Q(description__icontains=value)
            )
    
    def get_current_sort_by(self):
        return self.data.get('sort_by') or ''
    
    class Meta:
        model = Item
        fields = ['q','category','hyper_category','price_min','price_max']