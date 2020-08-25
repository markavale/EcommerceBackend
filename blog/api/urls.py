from django.urls import path
from .views import (blog_detail_view, blog_list,BlogListView #blog_create_view,
            #blog_update_view, blog_delete_view
)

app_name = 'blog'

urlpatterns = [
    path('',blog_list, name='blog-list'),
    path('<slug>/',blog_detail_view, name='blog-detail'),
    path('list',BlogListView.as_view(), name='blogs'),
    #path('<slug>/update/',blog_update_view, name='blog-update'),
    #path('<slug>/delete/',blog_delete_view, name='blog-delete'),
    #path('create/',blog_create_view, name='blog-create'),
]