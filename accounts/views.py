# accounts/views.py
from django.shortcuts import render
from .forms import RegisterForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth import login as auth_login


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'accounts/form.html'
    success_url = reverse_lazy('mypage')
    extra_context = {'is_register': True, 'submit': '회원가입', }

    def form_valid(self, form):
        response = super().form_valid(form)
        auth_login(self.request, self.object)
        return response


register = RegisterView.as_view()

login = LoginView.as_view(
    template_name='accounts/form.html',
    extra_context={'is_register': False, 'submit': '로그인', }
)

logout = LogoutView.as_view(
    next_page='/'
)


@login_required
def mypage(request):
    return render(request, 'accounts/mypage.html')
