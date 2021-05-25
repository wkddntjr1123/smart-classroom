from django.db import models


class Lecture(models.Model) :
    title = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    #student = models.ForeignKey()