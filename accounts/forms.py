# accounts/forms.py
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, ReadOnlyPasswordHashField


class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
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


class UserUpdateForm(UserChangeForm):
    user_id = forms.CharField(disabled=True, label='사용자 이름')
    password = ReadOnlyPasswordHashField(
        label='비밀번호', help_text='비밀번호 변경은 <a href="/accounts/password/">여기</a>서 가능합니다.')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = kwargs.get('instance', None)
        if instance is not None:
            self.fields['user_id'].initial = instance.username

    class Meta(UserChangeForm.Meta):
        model = get_user_model()
        fields = ['nickname', 'email', 'profile_img', 'introduce']
        labels = {
            'nickname': '닉네임',
            'email': '이메일',
            'profile_img': '프로필 사진',
            'introduce': '간단한 취미 소개'
        }

    field_order = ['user_id', 'password'] + Meta.fields
