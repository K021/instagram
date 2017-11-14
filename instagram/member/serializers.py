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
    token = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'nickname', 'img_profile', 'user_type', 'token',)

    @staticmethod
    def get_token(instance):
        return Token.objects.get_or_create(user=instance)[0].key

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

