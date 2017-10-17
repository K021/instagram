from django.db import models
from django.forms import Form

__all__ = (
    'Post',
    'PostComment',
)


class Post(models.Model):
    photo = models.ImageField(upload_to='post')
    title = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        title = self.title if self.title else f'Post#{self.pk}'
        return f'{title} ({self.photo})'


class PostComment(models.Model):
    post = models.ForeignKey(Post, related_name='comments')
    content = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        post_title = self.post.title if self.post.title else f'Post#{self.post.pk}'
        return f'{post_title}: (User.name) {self.content[0:50]}'


