from django.conf import settings
from django.db import models

__all__ = (
    'Post',
    'PostComment',
)


class PostManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().exclude(author=None)


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    photo = models.ImageField(upload_to='post')
    title = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = PostManager()

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        title = self.title if self.title else f'Post#{self.pk}'
        return f'{title} ({self.photo})'

    # def get_absolute_url(self):
    #     return f'/post/{self.pk}/'


class PostComment(models.Model):
    post = models.ForeignKey(Post, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    content = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        post_title = self.post.title if self.post.title else f'Post#{self.post.pk}'
        return f'{post_title}: ({author.username}) {self.content[0:50]}'
