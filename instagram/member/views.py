from django.contrib.auth import get_user_model, logout as dj_logout
from django.http import HttpResponse, request
from django.shortcuts import render, redirect
from member.forms import SignupForm, LoginForm

User = get_user_model()


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            form.login(request)
            return redirect('post_list')
    else:
        form = LoginForm()
    context = {
        'form': form,
    }
    return render(request, 'member/login.html', context)


def logout(request):
    dj_logout(request)
    return redirect('post_list')


def signup(request):
    if request.method == 'POST':
        # (기본)
        # username = request.POST.get('username')
        # password = request.POST.get('password')
        # (기본)
        form = SignupForm(request.POST)
        # (기본)
        # if username and password:
        # (기본)
        if form.is_valid():
            # 주어진 username의 User가 존재하는지 검사
            # if User.objects.filter(username=username).exists():
            #     return HttpResponse(f'Username {username} is already exist')
            # 없으면 User 생성
            form.signup()
            return redirect('post_list')
    else:
        form = SignupForm()
    context = {
        'form': form,
    }
    return render(request, 'member/signup.html', context)
