from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from authentication.models import User
from .models import Attendance
from professor.models import Lecture
import json


def myInfo(request) :
    return render(request,'student/my-info.html')


def myAttendance(request):
    myattend = Attendance.objects.filter(pupil=request.user)
    mylectureArr = []
    for lecture in myattend :
        mylectureArr.append(lecture)
        
    context = {"mylectureArr":mylectureArr}
    return render(request,'student/my-attendance.html',context)

def changeImage(request):
    user = User.objects.get(id=request.user.id)
    user.photo = request.FILES['image']
    user.save()
    
    return redirect('student:my-info')

def confirmAttendance(request,lecture_id ,weekNum):
    lecture = Lecture.objects.get(id=int(lecture_id)) #강의 객체
    attend = Attendance.objects.filter(course=lecture)  #강의 객체에 연결된 출석 객체들 (pupil속성에 수강생, state에 출석현황 저장)
     
    context={"title":lecture.title, "attend_obj":attend, "week":weekNum}
    return render(request,"student/confirm-attendance.html",context)

def enrolment(request):
    if request.method == 'POST' :
        data = json.loads(request.body)
        lecture_id = data['lecture_id']
       
        if(len(Attendance.objects.filter(pupil=request.user,course=Lecture.objects.get(id=lecture_id)))):
            return JsonResponse({"fail":True})
       
        newAttend = Attendance()
        newAttend.course = Lecture.objects.get(id=lecture_id)
        newAttend.pupil = request.user
        newAttend.week1 = 'yet'
        newAttend.week2 = 'yet'
        newAttend.week3 = 'yet'
        newAttend.week4 = 'yet'
        newAttend.save()
        return JsonResponse({"success":True})
        
    else :
        lectures = Lecture.objects.all()
    
        context_arr = []
        for lecture in lectures :
            attend = Attendance.objects.filter(course=lecture)
            context_arr.append([lecture,len(attend)])
        
        context = {"lecture_and_pupil":context_arr}
       
        return render(request,"student/enrolment.html",context)
    
