from django.db import models

__all__ = (
    'Post',
    'PostComment',
)


class Post(models.Model):
    photo = models.ImageField(upload_to='post')
    created_at = models.DateTimeField(auto_now_add=True)


class PostComment(models.Model):
    post = models.ForeignKey(Post)
    content = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)
