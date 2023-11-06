# main/views.py
from django.shortcuts import render
from blog.models import Category


def index(request):
    return render(request, 'main/index.html', {'category_list': Category.objects.all(), })


def about(request):
    return render(request, 'main/about.html', {'category_list': Category.objects.all(), })


def contact(request):
    return render(request, 'main/contact.html', {'category_list': Category.objects.all(), })
