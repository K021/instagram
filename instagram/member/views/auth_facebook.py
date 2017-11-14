import json
from typing import NamedTuple

import requests
from django.conf import settings
from django.contrib.auth import login as dj_login, authenticate
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.views import View

__all__ = (
    'FrontFacebookLogin',
    'facebook_login',
)


class FrontFacebookLogin(View):
    # access token 값을 저장하는 클래스
    class AccessTokenInfo(NamedTuple):
        access_token: str
        token_type: str
        expires_in: str

    # token 값의 유효성을 검사하기 위한 정보를 저장하는 클래스
    class DebugTokenInfo(NamedTuple):
        app_id: str
        application: str
        expires_at: int
        is_valid: bool
        issued_at: int
        scopes: list
        type: str
        user_id: str

    # User 정보를 담는 클래스
    class UserInfo:
        def __init__(self, data):
            self.id = data['id']
            self.email = data.get('email', '')
            self.url_picture = data['picture']['data']['url']

    # GET 요청이 들어왔을 때.
    def get(self, request):
        # http://developers.facebook.com/ 에서 만든 Facebook 애플리케이션 access 정보.
        app_id = settings.FACEBOOK_APP_ID
        app_secret_code = settings.FACEBOOK_APP_SECRET_CODE
        app_access_token = f'{app_id}|{app_secret_code}'
        code = request.GET['code']

        # token 을 받아오는 메서드
        def get_access_token_info(code):
            params = {
                'client_id': app_id,
                'client_secret': app_secret_code,
                'redirect_uri': '{scheme}://{host}{redirect_url}'.format(
                    scheme=request.scheme,
                    host=request.META['HTTP_HOST'],
                    redirect_url=reverse('member:front-facebook-login')
                ),
                'code': code,
            }
            response = requests.get('https://graph.facebook.com/v2.10/oauth/access_token', params=params)

            # **response.json()에 대하여
            # 1. json.loads(response.content) 와 같음
            # 2. 앞에 붙은 **는, json 정보를 key-value 로 집어 넣는 것을 의미한다.
            # AccessTokenInfo(access_token=response.json()['access_token'],
            #    'token_type'=response.json()['token_type.....
            return self.AccessTokenInfo(**response.json())

        # 받아온 토큰 값이 진짜 토큰인지 확인하는 메서드
        def get_debug_token_info(access_token):
            params = {
                'input_token': access_token,
                'access_token': app_access_token,
            }
            response = requests.get('https://graph.facebook.com/debug_token', params=params)
            return self.DebugTokenInfo(**response.json()['data'])

        # 토큰을 받아오고 디버그하는 메서드 실행
        token_info = get_access_token_info(code)
        access_token = token_info.access_token
        debug_token_info = get_debug_token_info(token_info.access_token)

        # 토큰을 사용해서 유저 정보 받아옴
        url_graph_user_info = 'https://graph.facebook.com/me'
        user_information_fields = ['id', 'name', 'picture', 'email']
        params_graph = {
            'fields': ','.join(user_information_fields),
            'access_token': access_token,
        }
        response = requests.get(url_graph_user_info, params_graph)
        result = response.json()
        user_info = self.UserInfo(data=result)

        # 현재 클래스는 프론트 측의 작업이므로, 유저 생성 없이 유저 아이디와 토큰만을 전달한다.
        data = {
            'facebook_user_id': user_info.id,
            'access_token': access_token,
        }
        return JsonResponse(data)


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

    # 토큰을 사용해서 유저 정보 받아오기
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
    if not User.objects.filter(username=username).exists():
        User.objects.create_user(
            user_type=User.USER_TYPE_FACEBOOK,
            username=username,
        )
    # 유저가 인증되면 유저 리턴하는 인증함
    user = authenticate(facebook_user_id=user_info.id)
    # 장고 내장 로그인을 이용할 때, 사용하는 Authentication Backend 를 명시해주어야 한다
    # 위에서 authenticate 를 거친 다음에는 backend 인자를 생략할 수 있다
    dj_login(request, user, backend='django.contrib.auth.backends.ModelBackend')
    return redirect('main')

    # print(request.GET)
    # print(request.POST)
    # get_string = '<br>'.join(['\t{}: {}'.format(key, value) for key, value in request.GET.items()])
    # post_string = '<br>'.join(['\t{}: {}'.format(key, value) for key, value in request.POST.items()])
    # return HttpResponse(f'GET:<br>{get_string}<br>POST:<br>{post_string}')
