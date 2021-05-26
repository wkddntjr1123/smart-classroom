from professor.models import Lecture
from django.db import models
from django.db.models.deletion import CASCADE, SET_DEFAULT
from authentication.models import User

# 출석 모델 : 주차, 유저FK, 강의FK, (하기 전, 출석, 지각, 결석) 값, 

class Attendance(models.Model):
    CHOICES = (('yet','yet'),('attend','attend'),('late','late'),('absent','absent'))
    
    week = models.CharField(max_length=100)
    pupil = models.ForeignKey(User, on_delete=CASCADE)
    state = models.CharField(max_length=100, choices=CHOICES, default='yet', blank=True, null=False)
    course = models.ForeignKey(Lecture, on_delete=CASCADE)
    
    def __str__(self) :
        return self.course.title