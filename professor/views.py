from django.http import request
from django.http.response import JsonResponse
from django.shortcuts import render,redirect
from .models import Lecture
from authentication.models import User
from student.models import Attendance
from imutils.video import VideoStream
from imutils.video import FPS
import face_recognition
import imutils
import pickle
import time
import cv2

def manageAttendance(request, lecture_id, weekNum) :
    lecture = Lecture.objects.get(id=int(lecture_id)) #강의 객체
    attend = Attendance.objects.filter(course=lecture)  #강의 객체에 연결된 출석 객체들 (pupil속성에 수강생, state에 출석현황 저장)
     
    context={"title":lecture.title, "attend_obj":attend, "week":weekNum, "lecture_id":lecture_id}
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
    
    
def autoAttend(request,lecture_id,week) :
    
    currentname = "unknown"
    encodingsP = "/home/pi/Desktop/smart_classroom/facial_recognition/encodings.pickle"
    cascade = "/home/pi/Desktop/smart_classroom/facial_recognition/haarcascade_frontalface_default.xml"
    
    print("[INFO] loading encodings + face detector...")
    data = pickle.loads(open(encodingsP, "rb").read())
    detector = cv2.CascadeClassifier(cascade)
        
    print("[INFO] starting video stream...")
    vs = VideoStream(usePiCamera=True).start()
    time.sleep(2.0)
    
    fps = FPS().start()
    
    while True:
    
        frame = vs.read()
        frame = imutils.resize(frame, width=500)
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        rects = detector.detectMultiScale(gray, scaleFactor=1.1, 
            minNeighbors=5, minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE)

        boxes = [(y, x + w, y + h, x) for (x, y, w, h) in rects]

        encodings = face_recognition.face_encodings(rgb, boxes)
        names = []

        for encoding in encodings:
            matches = face_recognition.compare_faces(data["encodings"],
                encoding)
            name = "Unknown"

            if True in matches:
                matchedIdxs = [i for (i, b) in enumerate(matches) if b]
                counts = {}

                for i in matchedIdxs:
                    name = data["names"][i]
                    counts[name] = counts.get(name, 0) + 1

                name = max(counts, key=counts.get)
                
                if currentname != name:
                    currentname = name
            
            #names에 인식된 학번이 담김
            names.append(name)

        for ((top, right, bottom, left), name) in zip(boxes, names):
            cv2.rectangle(frame, (left, top), (right, bottom),
                (0, 255, 225), 2)
            y = top - 15 if top - 15 > 15 else top + 15
            cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
                .8, (0, 255, 255), 2)

        cv2.imshow("Facial Recognition is Running", frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            break

        fps.update()
    
    fps.stop()
    print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
    print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

    # do a bit of cleanup
    cv2.destroyAllWindows()
    vs.stop()

    print(names)
    
    names = []
    alldata = Attendance.objects.filter(course=Lecture.objects.get(id=lecture_id)) # 해당 과목 Attendence를 모두 가져옴
    
    #만약 Attendece정보가 존재하면
    if(len(alldata)) :
        for data in alldata : #모든 attendence를 순회하면서
            
            if(week == 1) :  #1주차
                data.week1 = "absent"  #현재 주차의 출석을 모두 결석으로 처리한 후
                if data.pupil.username in names : #만약 names에 학번이 존재하면(얼굴인식됐다면)
                    data.week1 = "attend"    #출석 처리           
            if(week == 2) :
                data.week2 = "absent"  
                if data.pupil.username in names : 
                    data.week2 = "attend" 
            if(week == 3) :
                data.week3 = "absent"  
                if data.pupil.username in names : 
                    data.week3 = "attend"
            if(week == 4) :
                data.week4 = "absent"  
                if data.pupil.username in names : 
                    data.week4 = "attend"         

            data.save() #결과 db에 저장
                
    return JsonResponse({"success": True})