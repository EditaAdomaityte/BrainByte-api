from django.db import models

class QuestionCategory(models.Model):
    question = models.ForeignKey("Question", on_delete=models.CASCADE,)
    category = models.ForeignKey("Category", on_delete=models.DO_NOTHING, )
