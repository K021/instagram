import json
from pprint import pprint
from typing import NamedTuple

import requests
from django.conf import settings
from django.contrib.auth import get_user_model, logout as dj_logout, login as dj_login, authenticate
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from member.forms import SignupForm, LoginForm, ProfileForm
from post.models import Post, PostComment

User = get_user_model()

__all__ = (
    'login',
    'logout',
    'signup',
)

# 프론트에서 우리에게 페이스북 토큰 값을 넘겨주는 기능을 구현해본 클래스이다.


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