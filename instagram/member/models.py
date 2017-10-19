from django.contrib.auth.models import AbstractUser, UserManager as DjangoUserManager
from django.db import models


class UserManager(DjangoUserManager):
    def create_superuser(self, *args, **extra_fields):
        return super().create_superuser(
            # 내가 넣으려는 조건,
            *args, **extra_fields
        )


class User(AbstractUser):
    img_profile = models.ImageField(upload_to='user', blank=True)

    objects = UserManager()

    # terminal 에서 ./manage.py createsuperuser 명령시 요구할 필드
    REQUIRED_FIELDS = AbstractUser.REQUIRED_FIELDS + []
