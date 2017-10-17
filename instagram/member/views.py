from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import render

from member.forms import SignupForm

User = get_user_model()


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
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            # 주어진 username의 User가 존재하는지 검사
            if User.objects.filter(username=username).exists():
                return HttpResponse(f'Username {username} is already exist')
            # 없으면 User 생성
            User.objects.create_user(
                username=username,
                password=password,
            )
            return HttpResponse(f'Username:{username},\nPassword:{password}')

    form = SignupForm()
    context = {
        'form': form,
    }
    return render(request, 'member/signup.html', context)
