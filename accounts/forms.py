# accounts/forms.py
from .models import User
from django.contrib.auth.forms import UserCreationForm


class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'nickname', 'email', 'profile_img', 'introduce']
        labels = {
            'nickname': '닉네임',
            'email': '이메일',
            'profile_img': '프로필 사진',
            'introduce': '취미 소개'
        }
