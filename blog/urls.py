from django.urls import path
from .views import *

app_name = 'blog'

urlpatterns = [
    path('blog-list/' , BlogListView.as_view(), name='blog-list'),
    path('blog-detail<str:slug>/' , BlogDetailView.as_view(), name='blog-detail'),
    path('blog-create/' , BlogCreateView.as_view(), name='blog-create'),
    path('blog-update<str:slug>/' , BlogUpdateView.as_view(), name='blog-update'),
    path('blog-delete<str:slug>/' , BlogDeleteView.as_view(), name='blog-delete'),
    path('comment-delete<int:id>/' , comment_delete , name='comment-delete'),
    path('comment-reply<int:id>/' , comment_reply , name='comment-reply'),
]