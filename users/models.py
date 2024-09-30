from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {"blank": True, "null": True}


class User(AbstractUser):
    username = None
    email = models.EmailField(verbose_name='email')
    phone = models.CharField(unique=True, max_length=35, verbose_name='телефон')
    nickname = models.CharField(max_length=50, unique=True, verbose_name='ник')
    avatar = models.ImageField(upload_to="avatar/", default="avatar/new_preview.jpg")
    summ_subscription = models.PositiveIntegerField(verbose_name='цена за подписку', **NULLABLE)
    token = models.CharField(max_length=100, verbose_name='token', **NULLABLE)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.phone

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"
