from django.db import models


# Create your models here.
class Foobar(models.Model):
    name = models.CharField(max_length=50)
