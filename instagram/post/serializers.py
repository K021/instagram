from rest_framework import serializers

from member.serializers import UserSerializer
from .models import Post


class PostSerializer(serializers.ModelSerializer):
    # author = serializers.ReadOnlyField(source='author.pk')
    title = serializers.ReadOnlyField
    # api 로 만들 때, 유저 오브젝트로 보내는 것이 중요하다
    author = UserSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ('pk', 'author', 'photo', 'title')
