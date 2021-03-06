from django import forms
from django.contrib.auth import get_user_model, authenticate, login as django_login
from django.contrib.auth.forms import UserCreationForm

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

    # self.user 할당
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        # 해당 정보의 유저가 존재하는지 판단
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

# 기존 SignupForm
# class SignupForm(forms.Form):
#     username = forms.CharField(
#         widget=forms.TextInput(
#             attrs={
#                 'class': 'form-control',
#             }
#         )
#     )
#     password = forms.CharField(
#         widget=forms.PasswordInput(
#             attrs={
#                 'class': 'form-control',
#             }
#         ),
#     )
#     password_validation = forms.CharField(
#         widget=forms.PasswordInput(
#             attrs={
#                 'class': 'form-control',
#             }
#         ),
#     )
#
#     # clean_<field_name>: __getattr__ 매직메서드 사용. https://corikachu.github.io/articles/python/python-magic-method
#     # 실제 Form class를 타고 들어간 forms/forms.py에선 파이썬 내장함수인 getattr()을 사용한다
#     def clean_username(self):
#         data = self.cleaned_data['username']
#         if User.objects.filter(username=data).exists():
#             raise forms.ValidationError('Already existing username')
#         return data
#
#     def clean_password_validation(self):
#         password = self.cleaned_data['password']
#         password_validation = self.cleaned_data['password_validation']
#         if password != password_validation:
#             raise forms.ValidationError('Check your password again')
#         return password
#
#     def signup(self):
#         if self.is_valid():
#             username = self.cleaned_data.get('username')
#             password = self.cleaned_data.get('password')
#             user = User.objects.create_user(
#                 username=username,
#                 password=password,
#             )
#             return user
#         else:
#             raise forms.ValidationError('Invalid User')


class SignupForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        class_update_fields = ('password1', 'password2')
        for field in class_update_fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
            })

    class Meta:
        model = User
        fields = (
            'username',
            'nickname',
            'img_profile',
        )
        widgets = {
            'username': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'nickname': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            # 얘는 알아서 해줘서 딱히 필요 없다고 함
            'img_profile': forms.ClearableFileInput(
                attrs={
                    'class': 'form-control'
                }
            ),
        }


class ProfileForm(forms.Form):
    nickname = forms.CharField(
        initial='nickname',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    img_profile = forms.ImageField(
        widget=forms.ClearableFileInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    introduction = forms.CharField(
        initial='',
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'rows': '2',
            }
        )
    )

    def update(self, user):
        nickname = self.cleaned_data['nickname']
        img_profile = self.cleaned_data['img_profile']
        introduction = self.cleaned_data['introduction']
        if nickname:
            user.nickname = nickname
        if img_profile:
            user.img_profile = img_profile
        if introduction:
            user.introduction = introduction
        user.save()
