from django.db import models
from django.contrib.auth.models import User

class Question(models.Model):
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING,)
    body = models.CharField(max_length=255,)
    answer = models.BooleanField()