# blog/views.py
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from .models import Post, Category, Tag, Comment
from .forms import PostForm, CommentForm
from django.utils.text import slugify
from django.db.models import Q
from django.urls import reverse_lazy
import json


class PostList(ListView):
    model = Post
    ordering = '-pk'

    def get_context_data(self, **kwargs):
        context = super(PostList, self).get_context_data(**kwargs)
        context['category_list'] = Category.objects.all().order_by('name')
        context['no_category_post_count'] = Post.objects.filter(
            category=None).count()
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        search_keyword = self.request.GET.get('q')
        if search_keyword:
            queryset = queryset.filter(Q(title__icontains=search_keyword) | Q(
                content__icontains=search_keyword)).distinct()
        return queryset


class PostDetail(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data(**kwargs)
        context['comment_form'] = CommentForm
        return context

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        post = Post.objects.get(pk=pk)
        post.view_count += 1
        post.save()
        return super().get_object(queryset)


class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm

    def form_valid(self, form):
        current_user = self.request.user
        if current_user.is_authenticated:
            form.instance.author = current_user
            response = super(PostCreate, self).form_valid(form)
            tags_str = self.request.POST.get('tags_str')
            if tags_str:
                tags_str = tags_str.strip()
                tags_list = tags_str.split(',')
                for t in tags_list:
                    t = t.strip()
                    tag, is_tag_created = Tag.objects.get_or_create(name=t)
                    if is_tag_created:
                        tag.slug = slugify(t, allow_unicode=True)
                        tag.save()
                    self.object.tags.add(tag)
            return response
        else:
            return redirect('/blog/')


class PostUpdate(UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm

    def test_func(self):
        return self.get_object().author == self.request.user

    def form_valid(self, form):
        response = super(PostUpdate, self).form_valid(form)
        tags_str = self.request.POST.get('tags_str')
        if tags_str:
            tags_str = tags_str.strip()
            tags_list = tags_str.split(',')
            for t in tags_list:
                t = t.strip()
                tag, is_tag_created = Tag.objects.get_or_create(name=t)
                if is_tag_created:
                    tag.slug = slugify(t, allow_unicode=True)
                    tag.save()
                self.object.tags.add(tag)
        return response


class PostDelete(UserPassesTestMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('post_list')

    def test_func(self):
        return self.get_object().author == self.request.user


@login_required
def comment_new(request, pk):
    post = Post.objects.get(pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect(comment.get_absolute_url())
        else:
            form = CommentForm()
        return render(request, 'blog/comment_form.html', {'form': form})


@login_required
def comment_edit(request, pk):
    comment = Comment.objects.get(pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid() and comment.author == request.user:
            form.save()
            return redirect(comment.post.get_absolute_url())
        else:
            return HttpResponse('You are not allowed to edit this comment')

    else:
        form = CommentForm(instance=comment)
        return render(request, 'blog/comment_form.html', {'form': form})

# class CommentUpdate(UserPassesTestMixin, UpdateView):
#     model = Comment
#     form_class = CommentForm
#     extra_context = {'is_write': False}

#     def test_func(self):
#         return self.get_object().author == self.request.user


@login_required
def comment_del(request, pk):
    comment = Comment.objects.get(pk=pk)
    if comment.author == request.user:
        comment.delete()
        return redirect(comment.post.get_absolute_url())
    else:
        return HttpResponse('You are not allowed to delete this comment')


post_list = PostList.as_view()
post_detail = PostDetail.as_view()
write = PostCreate.as_view()
edit = PostUpdate.as_view()
delete = PostDelete.as_view()
# comment_edit = CommentUpdate.as_view()


def category_search(request, slug):
    category = Category.objects.get(slug=slug)
    context = {
        'post_list': Post.objects.filter(category=category).order_by('-pk'),
        'no_category_post_count': Post.objects.filter(category=None).count(),
        'category': category,
        'category_list': Category.objects.all().order_by('name'),
    }
    return render(request, 'blog/post_list.html', context)


def tag_search(request, slug):
    tag = Tag.objects.get(slug=slug)
    post_list = tag.post_set.all()
    context = {
        'post_list': post_list,
        'no_category_post_count': Post.objects.filter(category=None).count(),
        'tag': tag,
        'category_list': Category.objects.all().order_by('name'),
    }
    return render(request, 'blog/post_list.html', context)


@login_required
def post_like(request, id):
    post = Post.objects.get(id=id)
    user = request.user
    if user in post.like.all():
        post.like.remove(user)
        is_like_now = False
    else:
        post.like.add(user)
        is_like_now = True
    context = {'likeCount': post.like.count(), 'isLikeNow': is_like_now}
    return JsonResponse(context)


@login_required
def comment_like(request, id):
    comment = Comment.objects.get(id=id)
    user = request.user
    if user in comment.like.all():
        comment.like.remove(user)
        is_like_now = False
    else:
        comment.like.add(user)
        is_like_now = True
    context = {'likeCount': comment.like.count(), 'isLikeNow': is_like_now}
    return JsonResponse(context)
