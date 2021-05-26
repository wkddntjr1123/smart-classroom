from typing import Awaitable
from professor.models import Lecture
from django.db import models
from django.db.models.deletion import CASCADE, SET_DEFAULT
from authentication.models import User

class Attendance(models.Model):
    CHOICES = (('yet','yet'),('attend','attend'),('absent','absent'))
    
    pupil = models.ForeignKey(User, on_delete=CASCADE)
    course = models.ForeignKey(Lecture, on_delete=CASCADE)
    week1 = models.CharField(max_length=100, choices=CHOICES, default='yet', blank=True, null=False)
    week2 = models.CharField(max_length=100, choices=CHOICES, default='yet', blank=True, null=False)
    week3 = models.CharField(max_length=100, choices=CHOICES, default='yet', blank=True, null=False)
    week4 = models.CharField(max_length=100, choices=CHOICES, default='yet', blank=True, null=False)
    
    def __str__(self) :
        return self.pupil.name + "/" + self.course.title 
    
