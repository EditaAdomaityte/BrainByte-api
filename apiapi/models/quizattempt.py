from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models

class QuizAttempt(models.Model):
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING,)
    category = models.ForeignKey("Category", on_delete=models.DO_NOTHING,)
    question_count = models.IntegerField(validators=[MinValueValidator(1)],)
    created_date = models.DateField(auto_now_add=True)
