import json
from pprint import pprint
from typing import NamedTuple

import requests
from django.conf import settings
from django.contrib.auth import get_user_model, logout as dj_logout, login as dj_login
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from member.forms import SignupForm, LoginForm, ProfileForm
from post.models import Post, PostComment

User = get_user_model()


def login(request):
    # if 'HTTP_REFERER' not in request.GET:

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            form.login(request)
            pk = request.GET["post_pk"]
            # 로그아웃 상태로 댓글을 달았을 때, 로그인이 성공하면 댓글 생성
            if 'comment' in request.GET:
                comment = request.GET["comment"]
                if comment:
                    post = Post.objects.get(pk=pk)
                    PostComment.objects.create(
                        post=post,
                        author=User.objects.get(username=form.cleaned_data['username']),
                        content=comment,
                    )
            url = request.GET['url'] + f'#post.{pk}'
            return redirect(url) if url else redirect('main')
    else:
        form = LoginForm()
    # login view get 호출시 기본 값
    context = {
        'form': form,
        'url': request.META['HTTP_REFERER'],    # login 을 호출한 페이지 url
        'post_pk': '',
        'comment': '',
        'facebook_app_id': settings.FACEBOOK_APP_ID,
        'facebook_scope': settings.FACEBOOK_SCOPE,
    }
    # (비로그인 댓글 작성시 실행)
    # url get parameter 에 해당 값이 있으면 context 에 넣어 줌
    for param in ['url', 'post_pk', 'comment']:
        if param in request.GET:
            context[param] = request.GET[param]
    return render(request, 'member/login.html', context)


def logout(request):
    dj_logout(request)
    url = request.META['HTTP_REFERER']
    return redirect(url)


def signup(request):
    if request.method == 'POST':
        # (기본)
        # username = request.POST.get('username')
        # password = request.POST.get('password')
        # (기본)
        form = SignupForm(request.POST, request.FILES)
        # (기본)
        # if username and password:
        # (기본)
        if form.is_valid():
            # 주어진 username의 User가 존재하는지 검사
            # if User.objects.filter(username=username).exists():
            #     return HttpResponse(f'Username {username} is already exist')
            # 없으면 User 생성
            user = form.save()
            # user = form.signup()
            dj_login(request, user)
            return redirect('main')
    else:
        form = SignupForm()
    context = {
        'form': form,
    }
    return render(request, 'member/signup.html', context)

# def user_post(request):
#     post = Post.objects.filter(author=request.user)


def facebook_login(request):
    class AccessTokenInfo(NamedTuple):
        access_token: str
        token_type: str
        expires_in: str

    class DebugTokenInfo(NamedTuple):
        app_id: str
        application: str
        expires_at: int
        is_valid: bool
        issued_at: int
        scopes: list
        type: str
        user_id: str

    class UserInfo:
        def __init__(self, data):
            self.id = data['id']
            self.email = data.get('email', '')
            self.url_picture = data['picture']['data']['url']

    app_id = settings.FACEBOOK_APP_ID
    app_secret_code = settings.FACEBOOK_APP_SECRET_CODE
    app_access_token = f'{app_id}|{app_secret_code}'
    code = request.GET['code']

    def get_access_token_info(code):
        params = {
            'client_id': app_id,
            'client_secret': app_secret_code,
            'redirect_uri': '{scheme}://{host}{relative_url}'.format(
                scheme=request.scheme,
                host=request.META['HTTP_HOST'],
                relative_url=reverse('member:facebook_login')
            ),
            'code': code,
        }
        response = requests.get('https://graph.facebook.com/v2.10/oauth/access_token', params=params)
        return AccessTokenInfo(**json.loads(response.content))

    def get_debug_token_info(access_token):
        params2 = {
            'input_token': access_token,
            'access_token': app_access_token,
        }
        response2 = requests.get('https://graph.facebook.com/debug_token', params=params2)
        return DebugTokenInfo(**response2.json()['data'])

    token_info = get_access_token_info(code)
    access_token = token_info.access_token
    debug_token_info = get_debug_token_info(token_info.access_token)

    url_graph_user_info = 'https://graph.facebook.com/me'
    user_information_fields = ['id', 'name', 'picture', 'email']
    params_graph = {
        'fields': ','.join(user_information_fields),
        'access_token': access_token,
    }
    response = requests.get(url_graph_user_info, params_graph)
    result = response.json()
    user_info = UserInfo(data=result)

    # 페이스북으로 가입한 유저의 username.
    # user_info.id 값은 무작위 숫자가 나온다.
    username = f'fb_{user_info.id}'
    if User.objects.filter(username=username).exists():
        user = User.objects.get(username=username)
    else:
        user = User.objects.create_user(
            user_type=User.USER_TYPE_FACEBOOK,
            username=username,
        )
    dj_login(request, user)
    return redirect('main')

    # print(request.GET)
    # print(request.POST)
    # get_string = '<br>'.join(['\t{}: {}'.format(key, value) for key, value in request.GET.items()])
    # post_string = '<br>'.join(['\t{}: {}'.format(key, value) for key, value in request.POST.items()])
    # return HttpResponse(f'GET:<br>{get_string}<br>POST:<br>{post_string}')


def profile(request):
    if not request.user.is_authenticated:
        return redirect('member:login')
    posts = Post.objects.filter(author=request.user)
    context = {
        'posts': posts,
    }
    return render(request, 'member/profile.html', context)


def profile_update(request):
    user = request.user
    if not user.is_authenticated():
        return redirect('member:login')
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        form.is_valid()
        form.update(user)
        return redirect('member:profile')
    else:
        form = ProfileForm(
            initial={
                'nickname': user.nickname,
                'introduction': user.introduction,
            }
        )
    context = {
        'form': form,
    }
    return render(request, 'member/profile_update.html', context)
