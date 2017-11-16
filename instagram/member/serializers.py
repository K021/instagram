from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.authtoken.models import Token

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # 전부 오게 하고 싶은 경우 '__all__'
        fields = ('pk', 'nickname', 'img_profile', 'user_type', 'introduction')


class SignupSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'nickname', 'img_profile', 'user_type', 'token',)

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError("Incorrect password")
        return data

    def create(self, validated_data):
        # self.meta.model.objects.create_user와 정확히 같다.
        return User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password1'],
            nickname=validated_data['nickname'],
            img_profile=validated_data['img_profile'],
            user_type=validated_data['user_type'],
        )

    # to_representation 함수는 serializing 에서 마지막에 실행되는 함수로 (강사님의 추측. 함수를 직접 실행해보고 알았다.)
    # 최종적으로 dictionary 를 만들어준다
    def to_representation(self, instance):
        ret = super().to_representation()
        data = {
            'user': ret,
            'token': instance.token,
        }
        return data
