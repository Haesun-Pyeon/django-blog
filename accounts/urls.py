# accounts/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name='register'),
    path('mypage/', views.mypage, name='mypage'),
    path('edit/', views.user_edit, name='user_edit'),
    path('password/', views.password_edit, name='password_edit'),
    path('delete/<int:pk>/', views.user_delete, name='user_delete'),
]
