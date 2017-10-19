from django import forms
from django.contrib.auth import get_user_model, authenticate, login as django_login

User = get_user_model()


class LoginForm(forms.Form):
    """
    is_valid()에서 주어진 username/password 를 사용한 authenticate 실행
    """
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
            }
        )
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        self.user = authenticate(
            username=username,
            password=password,
        )
        if self.user is None:
            raise forms.ValidationError('Invalid user information')
        else:
            setattr(self, 'login', self._login)

    def _login(self, request):
        """
        django.contrib.auth.login(request) 실행

        :param request: django.contrib.auth.login()에 주어진 HttpResponse 객체
        :return:
        """
        django_login(request, self.user)


class SignupForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
            }
        ),
    )
    password_validation = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
            }
        ),
    )

    # clean_<field_name>: __getattr__ 매직메서드 사용. https://corikachu.github.io/articles/python/python-magic-method
    # 실제 Form class를 타고 들어간 forms/forms.py에선 파이썬 내장함수인 getattr()을 사용한다
    def clean_username(self):
        data = self.cleaned_data['username']
        if User.objects.filter(username=data).exists():
            raise forms.ValidationError('Already existing username')
        return data

    def clean_password_validation(self):
        password = self.cleaned_data['password']
        password_validation = self.cleaned_data['password_validation']
        if password != password_validation:
            raise forms.ValidationError('Check your password again')
        return password

    def signup(self):
        if self.is_valid():
            username = self.cleaned_data.get('username')
            password = self.cleaned_data.get('password')
            User.objects.create_user(
                username=username,
                password=password,
            )
        else:
            raise forms.ValidationError('Invalid User')

