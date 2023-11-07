# main/views.py
from django.shortcuts import render
from blog.models import Category, Post


def index(request):
    context = {
        'category_list': Category.objects.all(),
        'popular': Post.objects.all().order_by('-view_count')[0:1],
        'popular_list1': Post.objects.all().order_by('-view_count')[1:3],
        'popular_list2': Post.objects.all().order_by('-view_count')[3:5],
    }
    return render(request, 'main/index.html', context)


def about(request):
    return render(request, 'main/about.html', {'category_list': Category.objects.all(), })


def contact(request):
    return render(request, 'main/contact.html', {'category_list': Category.objects.all(), })
