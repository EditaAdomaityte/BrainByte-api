from django.db import models
from .quizattempt import QuizAttempt
from.question import Question

class QuizResponse(models.Model):
    quizattempt = models.ForeignKey(QuizAttempt, on_delete=models.DO_NOTHING, related_name="quiz")
    question = models.FForeignKey(Question, on_delete=models.DO_NOTHING, related_name="question")
    user_answer = models.BooleanField()
    is_correct = models.BooleanField()