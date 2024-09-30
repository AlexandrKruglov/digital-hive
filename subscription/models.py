from django.db import models

from users.models import User

NULLABLE = {"blank": True, "null": True}


# Create your models here.
class Payments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь')
    date_pay = models.DateField(auto_now_add=True, verbose_name='дата оплаты')
    summ = models.PositiveIntegerField(verbose_name='сумма оплаты')
    link = models.URLField(max_length=400, **NULLABLE, verbose_name='ссылка на оплату')
    session_id = models.CharField(max_length=200, **NULLABLE, verbose_name='id session')

    def __str__(self):
        return f'{self.link} {self.session_id}'

    class Meta:
        verbose_name = 'платеж'
        verbose_name_plural = 'платежи'


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь')
    subscribe_to_user = models.OneToOneField(User, on_delete=models.DO_NOTHING, related_name="author",
                                             verbose_name='подписка на автора')
    is_active = models.BooleanField(default=False, verbose_name='активна')

    def __str__(self):
        return f'{self.user} - {self.subscribe_to_user} '

    class Meta:
        unique_together = ('user', 'subscribe_to_user',)
        verbose_name = 'подписка'
        verbose_name_plural = 'подписки'
