from django.db import models
from django.utils import timezone

class Member(models.Model):
    user_id = models.IntegerField(null=True, default=0)

    user_name = models.CharField(max_length=100, null=False)
    user_email = models.CharField(max_length=100, null=False)

    user_type = models.SmallIntegerField(null=True) # 1: PT쌤 2: 일반회원

    trainer_group = models.IntegerField(null=False, default=0) # PT쌤의 고유 ID

    user_height = models.FloatField(null=True) # 소수점 이하 3자리수의 999개까지 지정
    user_weight = models.FloatField(null=True) # 소수점 이하 3자리수의 999개까지 지정

    user_status = models.SmallIntegerField(null=False, default=1) # 활동 회원 체크 1: 활동 2: 탈퇴
    user_view = models.SmallIntegerField(null=False, default=1) # 유저 삭제 체크

    user_gender = models.SmallIntegerField(null=True) # 유저 성별 1: 남자 2: 여자

    create_date = models.DateTimeField(null=False, auto_now_add=True)
    update_date = models.DateTimeField(null=True)

    
