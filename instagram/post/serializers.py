from rest_framework import serializers

from .models import Post


class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.pk')
    title = serializers.ReadOnlyField

    class Meta:
        model = Post
        fields = ('pk', 'author', 'photo', 'title')
