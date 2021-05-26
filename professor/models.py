from django.db import models
from django.db.models.deletion import CASCADE
from authentication.models import User

#강의 모델 : 강의명, 듣는 학생, 강의날(월요일 1교시 포맷), 강의자
class Lecture(models.Model) :
    
    title = models.CharField(max_length=100)
    period = models.CharField(max_length=50)
    teacher = models.ForeignKey(User, on_delete=CASCADE, related_name="teacher_set")    #역참조 이름을 _set에서 변경(충돌 방지)
    
    def __str__(self) :
        return self.title