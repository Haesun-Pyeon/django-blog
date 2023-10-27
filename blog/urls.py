# blog/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('<int:pk>/', views.post_detail, name='post_detail'),

    path('write/', views.write, name='post_write'),
    path('edit/<int:pk>', views.edit, name='post_edit'),
    path('delete/<int:pk>', views.delete, name='post_delete'),

    path('<int:pk>/comment-new/', views.comment_new, name='comment_new'),
    path('comment-edit/<int:pk>/', views.comment_edit, name='comment_edit'),
    path('comment-del/<int:pk>/', views.comment_del, name='comment_del'),

    path('category/<str:slug>/', views.category_page, name='category_page'),
    path('tag/<str:slug>/', views.tag_page, name='tag_page'),
]
