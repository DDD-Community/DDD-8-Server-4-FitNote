from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


class User(AbstractUser):
    username = None

    email = models.EmailField(_('email address'), unique=True)

    user_name = models.CharField(max_length=100, null=False)
    user_type = models.SmallIntegerField(null=True)

    trainer_group = models.IntegerField(null=False, default=0)

    user_height = models.FloatField(null=True) # 소수점 이하 3자리수의 999개까지 지정
    user_weight = models.FloatField(null=True)

    user_status = models.SmallIntegerField(null=False, default=1)
    user_view = models.SmallIntegerField(null=False, default=1)
    user_gender = models.SmallIntegerField(null=True)

    create_date = models.DateTimeField(null=False, auto_now_add=True)
    update_date = models.DateTimeField(null=False, auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    spouse_name = models.CharField(blank=True, max_length=100)
    date_of_birth = models.DateField(blank=True, null=True)
    

    def __str__(self):
        return self.email
