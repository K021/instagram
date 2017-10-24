import json
from pprint import pprint

import requests
from django.conf import settings
from django.contrib.auth import get_user_model, logout as dj_logout, login as dj_login
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from member.forms import SignupForm, LoginForm
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
    app_id = settings.FACEBOOK_APP_ID
    app_secret_code = settings.FACEBOOK_APP_SECRET_CODE
    app_access_token = f'{app_id}|{app_secret_code}'
    params = {
        'client_id': app_id,
        'client_secret': app_secret_code,
        'redirect_uri': '{scheme}://{host}{relative_url}'.format(
            scheme=request.scheme,
            host=request.META['HTTP_HOST'],
            relative_url=reverse('member:facebook_login')
        ),
        'code': request.GET['code'],
    }
    response = requests.get('https://graph.facebook.com/v2.10/oauth/access_token', params=params)
    content = json.loads(response.content)

    params2 = {
        'input_token': content['access_token'],
        'access_token': app_access_token,
    }
    response2 = requests.get('https://graph.facebook.com/debug_token', params=params2)
    content2 = response2.json()
    string = '<br>'.join(['\t{}: {}'.format(key, value) for key, value in content2.items()])
    return HttpResponse(string)

    # print(request.GET)
    # print(request.POST)
    # get_string = '<br>'.join(['\t{}: {}'.format(key, value) for key, value in request.GET.items()])
    # post_string = '<br>'.join(['\t{}: {}'.format(key, value) for key, value in request.POST.items()])
    # return HttpResponse(f'GET:<br>{get_string}<br>POST:<br>{post_string}')
