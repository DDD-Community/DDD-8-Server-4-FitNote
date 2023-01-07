from django.db import models
from django.utils import timezone

class Lesson(models.Model):
    user_id = models.IntegerField(null=False)
    name = models.CharField(max_length=200, default='')
    weight = models.CharField(max_length=100, default='0')
    count = models.IntegerField(default=0)
    set = models.IntegerField(default=0)
    completion = models.IntegerField(default=0)
    total_completion = models.IntegerField(default=0)
    view_yn = models.IntegerField(default=1)
    start_date = models.IntegerField(default=0)
    create_date = models.DateTimeField('date published', default=timezone.now)
