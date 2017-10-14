from django.db import models

__all__ = (
    'Post',
    'PostComment',
)


class Post(models.Model):
    MEDIA_CHOICES = (
        ('Audio', (
            ('vinyl', 'Vinyl'),
            ('cd', 'CD'),
        )
         ),
        ('Video', (
            ('vhs', 'VHS Tape'),
            ('dvd', 'DVD'),
        )
         ),
        ('unknown', 'Unknown'),
    )
    photo = models.ImageField(upload_to='post')
    text = models.CharField(max_length=50, choices=MEDIA_CHOICES, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def text_display(self):
        return self.get_text_display()


class PostComment(models.Model):
    post = models.ForeignKey(Post)
    content = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)
