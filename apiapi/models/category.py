from django.db import models


class Category(models.Model):

    name = models.CharField(max_length=55)

    class Meta:
        verbose_name = ("questioncategory")
        verbose_name_plural = ("questioncategories")