# blog/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('<int:pk>/', views.post_detail, name='post_detail'),

    path('write/', views.write, name='post_write'),
    path('edit/<int:pk>/', views.edit, name='post_edit'),
    path('delete/<int:pk>/', views.delete, name='post_delete'),

    path('<int:post>/comment-new/', views.comment_new, name='comment_new'),
    path('comment-edit/<int:pk>/', views.comment_edit, name='comment_edit'),
    path('comment-del/<int:pk>/', views.comment_del, name='comment_del'),

    path('category/<str:slug>/', views.category_search, name='category'),
    path('tag/<str:slug>/', views.tag_search, name='tag'),

    path('post-like/<int:id>/', views.post_like, name='post_like'),
    path('comment-like/<int:id>/', views.comment_like, name='comment_like'),
]
