from django.http import request
from django.shortcuts import render,redirect
from .models import Lecture
from authentication.models import User
from student.models import Attendance

def manageAttendance(request, lecture_id, week) :
    lecture = Lecture.objects.get(id=int(lecture_id)) #강의 객체
    attend = Attendance.objects.filter(course=lecture, week=week)  #강의 객체에 연결된 출석 객체들 (pupil속성에 수강생, state에 출석현황 저장)
    
    context={"title":lecture.title, "attend_obj":attend}
    return render(request,"professor/manage-attendance.html",context)

def manageLecture(request) :
    lectures = Lecture.objects.all()
    
    context_arr = []
    for lecture in lectures :
      attend = Attendance.objects.filter(course=lecture)
      context_arr.append([lecture,len(attend)])
    
    context = {"lecture_and_pupil":context_arr}
    return render(request, "professor/manage-lecture.html",context)

def createLecture(request):
    if request.method == 'POST' :
        title = request.POST.get('title')
        teacher_id = request.POST.get('teacher_id')
        full_period = request.POST.get('period')

        new_lecture = Lecture()
        new_lecture.title = title
        new_lecture.period = full_period
        new_lecture.teacher = User.objects.get(id=teacher_id)
        new_lecture.save()

        return redirect('professor:manage-lecture')
    
    else :
        return render(request,"professor/create-lecture.html")