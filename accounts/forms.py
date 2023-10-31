# accounts/forms.py
from .models import User
from django.contrib.auth.forms import UserCreationForm


class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'password1', 'password2',
                  'nickname', 'email', 'profile_img', 'introduce']
        labels = {
            'nickname': '닉네임',
            'email': '이메일',
            'profile_img': '프로필 사진',
            'introduce': '간단한 취미 소개'
        }

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['introduce'].widget.attrs['style'] = 'resize: none;'
