from django.contrib.auth.models import AbstractUser, UserManager as DjangoUserManager
from django.db import models


class UserManager(DjangoUserManager):
    def create_superuser(self, *args, **extra_fields):
        return super().create_superuser(
            # 내가 넣으려는 조건,
            *args, **extra_fields
        )


class User(AbstractUser):
    DEFAULT_IMG_PATH = 'default/profile.jpg'
    # facebook / django 유저 선택
    USER_TYPE_DJANGO = 'D'
    USER_TYPE_FACEBOOK = 'F'
    USER_TYPE = (
        (USER_TYPE_DJANGO, 'Django Login'),
        (USER_TYPE_FACEBOOK, 'Facebook Login'),
    )

    # field
    nickname = models.CharField('닉네임', max_length=50,)
    img_profile = models.ImageField(
        '프로필 이미지', upload_to='user', null=True,
        default=DEFAULT_IMG_PATH,)
    liked_posts = models.ManyToManyField(
        'post.Post', verbose_name='좋아요 포스트 목록',)
    stars = models.ManyToManyField(
        'User', symmetrical=False, through='Relation',
        verbose_name='follow',
        related_name='followers',)
    user_type = models.CharField(max_length=1, choices=USER_TYPE)
    introduction = models.CharField(max_length=100, blank=True,)

    objects = UserManager()

    # terminal 에서 ./manage.py createsuperuser 명령시 요구할 필드
    REQUIRED_FIELDS = AbstractUser.REQUIRED_FIELDS + []

    class Meta:
        verbose_name = '사용자'
        verbose_name_plural = f'{verbose_name} 목록'

    def like(self, post):
        self.liked_posts.add(post)

    def unlike(self, post):
        self.liked_posts.remove(post)

    def like_toggle(self, post):
        if self.liked_posts.filter(pk=post.pk).exists():
            self.unlike(post)
        else:
            self.like(post)

    def follow_toggle(self, user):
        if not isinstance(user, User):
            raise ValueError('Invalid argument. User type is required.')
        relation, created = self.myrelations_with_stars.get_or_create(star=user)
        if created:
            return True
        relation.delete()
        return False
        # 중개모델에서는 아래의 add, remove 사용 불가
        # if self.stars.filter(pk=user.pk).exists():
        #     self.stars.remove(user)
        # else:
        #     self.stars.add(user)

    def set_default_img_profile(self):
        self.img_profile.delete()
        self.img_profile = self.DEFAULT_IMG_PATH
        self.save()


class Relation(models.Model):
    RELATION_TYPE = (
        ('F', 'Following relation'),
        ('B', 'Blocking relation'),
    )
    follower = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='myrelations_with_stars'
    )
    star = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='myrelations_with_followers'
    )
    date = models.DateField(auto_now_add=True)
    relation_type = models.CharField(max_length=1, choices=RELATION_TYPE, default='FOLLOW')

    def __str__(self):
        return f'"{self.follower.username}" follows "{self.star.username}"'
