from typing import NamedTuple

import requests
from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from rest_framework import status, request
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.views import APIView

from member.serializers import UserSerializer, SignupSerializer

User = get_user_model()


class Login(APIView):
    def post(self, request, *args, **kwargs):
        print(request.data)
        username = request.data['username']
        password = request.data['password']

        user = authenticate(username=username, password=password)
        if user:
            token, is_token_created = Token.objects.get_or_create(user=user)
            data = {
                'token': token.key,
                'user': UserSerializer(user).data,
            }
            return Response(data, status=status.HTTP_200_OK)
        else:
            data = {
                'message': 'Invalid credentials'
            }
            return Response(data, status=status.HTTP_401_UNAUTHORIZED)


class Signup(APIView):
    # def post(self, request):
    #     # 회원 가입 후 토큰 생성, 유저 정보 및 토큰 키 반환
    #     username = request.data['username']
    #     password = request.data['password']
    #
    #     if User.objects.filter(username=username).exists():
    #         return Response(status=status.HTTP_400_BAD_REQUEST)
    #
    #     user = User.objects.create_user(username=username, password=password)
    #     token = Token.objects.create(user=user)
    #     data = {
    #         'token': token.key,
    #         'user': UserSerializer(user).data,
    #     }
    #     return Response(data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FacebookLogin(APIView):
    def post(self, request):
        # request.data 에 facebook_user_id 와 access_token 이 전달되어 옴
        print(request.data)

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

        # 받아온 토큰 값이 진짜 토큰인지 확인하는 메서드
        def get_debug_token_info(access_token):
            app_id = settings.FACEBOOK_APP_ID
            app_secret_code = settings.FACEBOOK_APP_SECRET_CODE
            app_access_token = f'{app_id}|{app_secret_code}'

            params = {
                'input_token': access_token,
                'access_token': app_access_token,
            }
            response = requests.get('https://graph.facebook.com/debug_token', params=params)
            return DebugTokenInfo(**response.json()['data'])

        debug_token_info = get_debug_token_info(request.data['access_token'])

        if debug_token_info.user_id != request.data['facebook_user_id']:
            raise APIException('페이스북 토큰의 사용자와 전달받은 facebook_user_id가 일치하지 않음')

        if not debug_token_info.is_valid:
            raise APIException('페이스북 토큰이 유효하지 않음')

        # FacebookBackend를 사용해서 유저 인증
        user = authenticate(facebook_user_id=request.data['facebook_user_id'])
        # 인증에 실패한 경우 페이스북유저 타입으로 유저를 만들어줌
        if not user:
            user = User.objects.create_user(
                username=f'fb_{request.data["facebook_user_id"]}',
                user_type=User.USER_TYPE_FACEBOOK,
            )
        # 유저 시리얼라이즈 결과를 Response
        data = {
            'user': UserSerializer(user).data,
            'token': user.token,
        }
        return Response(data)
