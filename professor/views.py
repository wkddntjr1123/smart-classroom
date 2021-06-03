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
    
    
def autoAttend(request) :
 
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
    return JsonResponse({"success":"fffds"})