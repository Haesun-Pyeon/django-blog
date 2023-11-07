# accounts/views.py
from blog.models import Category, Comment
from .forms import RegisterForm, UserUpdateForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth import login as auth_login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.views.generic import CreateView, TemplateView, UpdateView, DeleteView


class UserLoginView(LoginView):
    template_name = 'accounts/form.html'

    def get_context_data(self, **kwargs):
        context = super(UserLoginView, self).get_context_data(**kwargs)
        context['category_list'] = Category.objects.all()
        context['submit'] = '로그인'
        context['is_login'] = True
        return context


class UserLogoutView(LogoutView):
    next_page = '/'


class UserCreateView(CreateView):
    form_class = RegisterForm
    template_name = 'accounts/form.html'

    def get_context_data(self, **kwargs):
        context = super(UserCreateView, self).get_context_data(**kwargs)
        context['category_list'] = Category.objects.all()
        context['submit'] = '회원가입'
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        auth_login(self.request, self.object)
        messages.success(self.request, '회원가입이 완료되었습니다.')
        return response


class UserReadView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/mypage.html'

    def get_context_data(self, **kwargs):
        context = super(UserReadView, self).get_context_data(**kwargs)
        context['category_list'] = Category.objects.all()
        context['comment_list'] = Comment.objects.filter(
            author=self.request.user).order_by('-pk')
        context['comment_like_list'] = Comment.objects.filter(
            like=self.request.user).order_by('-pk')
        return context


class UserUpdateView(LoginRequiredMixin, UpdateView):
    form_class = UserUpdateForm
    template_name = 'accounts/form.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super(UserUpdateView, self).get_context_data(**kwargs)
        context['category_list'] = Category.objects.all()
        context['submit'] = '수정'
        context['is_edit'] = True
        return context

    def form_valid(self, form):
        messages.success(self.request, '회원정보 수정을 완료했습니다.')
        return super().form_valid(form)


class PasswordUpdateView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'accounts/form.html'
    success_url = reverse_lazy('mypage')

    def get_context_data(self, **kwargs):
        context = super(PasswordUpdateView, self).get_context_data(**kwargs)
        context['category_list'] = Category.objects.all()
        context['submit'] = '수정'
        context['is_edit'] = True
        return context

    def form_valid(self, form):
        messages.success(self.request, '비밀번호 변경을 완료했습니다.')
        return super().form_valid(form)


class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = get_user_model()
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        messages.success(self.request, '회원 탈퇴가 완료되었습니다.')
        return super().form_valid(form)


login = UserLoginView.as_view()
logout = UserLogoutView.as_view()
register = UserCreateView.as_view()
mypage = UserReadView.as_view()
user_edit = UserUpdateView.as_view()
password_edit = PasswordUpdateView.as_view()
user_delete = UserDeleteView.as_view()
