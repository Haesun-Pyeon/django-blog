# blog/views.py
from .models import Post, Category, Tag, Comment
from .forms import PostForm, CommentForm
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.db.models import Q
from django.utils.text import slugify
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView


class PostList(ListView):
    model = Post
    ordering = '-pk'

    def get_context_data(self, **kwargs):
        context = super(PostList, self).get_context_data(**kwargs)
        context['category_list'] = Category.objects.all().order_by('name')
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
        messages.success(self.request, '글 수정을 완료했습니다.')
        return response


class PostDelete(UserPassesTestMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('post_list')

    def test_func(self):
        return self.get_object().author == self.request.user

    def form_valid(self, form):
        messages.success(self.request, '글 삭제를 완료했습니다.')
        return super().form_valid(form)


class CommentCreate(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm

    def form_valid(self, form):
        post = Post.objects.get(pk=self.kwargs.get('post'))
        comment_form = form.save(commit=False)
        comment_form.author = self.request.user
        comment_form.post = post
        comment_form.save()
        return super().form_valid(form)


class CommentUpdate(UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm

    def test_func(self):
        return self.get_object().author == self.request.user


class CommentDelete(UserPassesTestMixin, DeleteView):
    model = Comment

    def test_func(self):
        return self.get_object().author == self.request.user

    def get_success_url(self):
        post = self.get_object().post
        return reverse_lazy('post_detail', kwargs={'pk': post.pk})


post_list = PostList.as_view()
post_detail = PostDetail.as_view()
write = PostCreate.as_view()
edit = PostUpdate.as_view()
delete = PostDelete.as_view()
comment_new = CommentCreate.as_view()
comment_edit = CommentUpdate.as_view()
comment_del = CommentDelete.as_view()


def category_search(request, slug):
    category = Category.objects.get(slug=slug)
    context = {
        'post_list': Post.objects.filter(category=category).order_by('-pk'),
        'category': category,
        'category_list': Category.objects.all().order_by('name'),
    }
    return render(request, 'blog/post_list.html', context)


def tag_search(request, slug):
    tag = Tag.objects.get(slug=slug)
    post_list = tag.post_set.all()
    context = {
        'post_list': post_list,
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
