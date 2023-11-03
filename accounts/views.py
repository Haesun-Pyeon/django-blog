# accounts/views.py
from .forms import RegisterForm, UserUpdateForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth import login as auth_login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.views.generic import CreateView, TemplateView, UpdateView, DeleteView


login = LoginView.as_view(
    template_name='accounts/form.html',
    extra_context={'is_login': True, 'submit': '로그인', }
)

logout = LogoutView.as_view(
    next_page='/'
)


class UserCreateView(CreateView):
    form_class = RegisterForm
    template_name = 'accounts/form.html'
    success_url = reverse_lazy('mypage')
    extra_context = {'submit': '회원가입', }

    def form_valid(self, form):
        response = super().form_valid(form)
        auth_login(self.request, self.object)
        messages.success(self.request, '회원가입이 완료되었습니다.')
        return response


class UserReadView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/mypage.html'


class UserUpdateView(LoginRequiredMixin, UpdateView):
    form_class = UserUpdateForm
    success_url = reverse_lazy('mypage')
    template_name = 'accounts/form.html'
    extra_context = {'submit': '수정', 'is_edit': True, }

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, '회원정보 수정을 완료했습니다.')
        return super().form_valid(form)


class PasswordUpdateView(LoginRequiredMixin, PasswordChangeView):
    success_url = reverse_lazy('user_edit')
    template_name = 'accounts/form.html'
    extra_context = {'submit': '수정', 'is_edit': True, }

    def form_valid(self, form):
        messages.success(self.request, '비밀번호 변경을 완료했습니다.')
        return super().form_valid(form)


class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = get_user_model()
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        messages.success(self.request, '회원 탈퇴가 완료되었습니다.')
        return super().form_valid(form)


register = UserCreateView.as_view()
mypage = UserReadView.as_view()
user_edit = UserUpdateView.as_view()
password_edit = PasswordUpdateView.as_view()
user_delete = UserDeleteView.as_view()
