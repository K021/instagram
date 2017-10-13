from django.db import models

# post 앱 생성


class Post(models.Model):
    photo = models.ImageField(upload_to='photo')
    created_at = models.DateTimeField(auto_now_add=True)


class PostComment:
    post = models.ForeignKey(Post)
    content = models.CharField()
    created_time = models.DateTimeField(auto_now_add=True)
