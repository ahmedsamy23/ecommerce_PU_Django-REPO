from django.urls import path
from .views import CategoryListView

app_name = 'categories'

urlpatterns = [
    path('<str:category>/', CategoryListView.as_view(), name='category-list'),
]

# hyper_category to url