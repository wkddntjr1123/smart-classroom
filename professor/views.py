from django.http import request
from django.shortcuts import render,redirect
from .models import Lecture
from authentication.models import User
from student.models import Attendance

def manageAttendance(request, lecture_id, weekNum) :
    lecture = Lecture.objects.get(id=int(lecture_id)) #강의 객체
    attend = Attendance.objects.filter(course=lecture)  #강의 객체에 연결된 출석 객체들 (pupil속성에 수강생, state에 출석현황 저장)
     
    context={"title":lecture.title, "attend_obj":attend, "week":weekNum}
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
    
'''
def 자동출석(request,recture_id,week) :
    1. 사진 촬영
    2. 유저증명사진 읽어와서 사진과 비교 진행해서 일치하는 유저객체를 배열에 저장(user_arr)
    3. alldata = Attendance.objects.filter(course=Lecture.objects.get(id=recture_id)) 해당 과목 Attendence모두 가져옴
    4. week값을 토대로 alldata.week{i} = "absent" 로 모두 결석처리
    5. for user in user_arr :
        alldata.filter(pupul=user)
        alldata.week{i} = "attend"
    6. return render() 로 화면 갱신
'''