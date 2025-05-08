from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models



class QuizAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey("Category", on_delete=models.DO_NOTHING,)
    question_count = models.IntegerField(validators=[MinValueValidator(1)],)
    created_date = models.DateField(auto_now_add=True)

    @property
    def result(self):
        from apiapi.models.quizresponse import QuizResponse
    
        responses=QuizResponse.objects.filter(quizattempt=self)
        correct_count=responses.filter(is_correct=True).count()
        if responses.count() > 0:
            # Format as percentage with 2 decimal places
            percentage = (correct_count / self.question_count) * 100
            return round(percentage, 2)
        return 0
