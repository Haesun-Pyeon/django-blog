# blog/views.py
from django.shortcuts import render


def post_list(request):
    return render(request, 'blog/post_list.html')


def post_detail(request):
    return render(request, 'blog/post_detail.html')


def write(request):
    return render(request, 'blog/write.html')


def edit(request):
    return render(request, 'blog/edit.html')


def delete(request):
    return render(request, 'blog/delete.html')


def comment_new(request):
    return render(request, 'blog/comment_new.html')


def comment_edit(request):
    return render(request, 'blog/comment_edit.html')


def comment_del(request):
    return render(request, 'blog/comment_del.html')


def category_page(request):
    return render(request, 'blog/category_page.html')


def tag_page(request):
    return render(request, 'blog/tag_page.html')
