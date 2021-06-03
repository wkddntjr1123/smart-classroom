from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from authentication.models import User
from .models import Attendance
from professor.models import Lecture
import json
import face_recognition
import cv2
import numpy as np

def myInfo(request) :
    return render(request,'student/my-info.html')


def myAttendance(request):
    myattend = Attendance.objects.filter(pupil=request.user)
    mylectureArr = []
    for lecture in myattend :
        mylectureArr.append(lecture)
        
    context = {"mylectureArr":mylectureArr}
    return render(request,'student/my-attendance.html',context)

def changeImage2(request):
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
    
def changeImage (request) :
    

    # This is a demo of running face recognition on live video from your webcam. It's a little more complicated than the
    # other example, but it includes some basic performance tweaks to make things run a lot faster:
    #   1. Process each video frame at 1/4 resolution (though still display it at full resolution)
    #   2. Only detect faces in every other frame of video.

    # PLEASE NOTE: This example requires OpenCV (the `cv2` library) to be installed only to read from your webcam.
    # OpenCV is *not* required to use the face_recognition library. It's only required if you want to run this
    # specific demo. If you have trouble installing it, try any of the other demos that don't require it instead.

    # Get a reference to webcam #0 (the default one)
    video_capture = cv2.VideoCapture(0)

    # Load a sample picture and learn how to recognize it.
    '''
    학습할 이미지
    '''
    obama_image = face_recognition.load_image_file("/home/pi/Desktop/media/training/201515300.png")
    obama_face_encoding = face_recognition.face_encodings(obama_image)[0]

    # Load a second sample picture and learn how to recognize it.
    #biden_image = face_recognition.load_image_file("biden.jpg")
    #biden_face_encoding = face_recognition.face_encodings(biden_image)[0]

    # Create arrays of known face encodings and their names
    known_face_encodings = [
        obama_face_encoding,
    #    biden_face_encoding
    ]
    '''
    라벨링
    '''
    known_face_names = [
        "201515300",
    #    "Joe Biden"
    ]

    # Initialize some variables
    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True

    while True:
        # Grab a single frame of video
        ret, frame = video_capture.read()

        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Only process every other frame of video to save time
        if process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"

                # # If a match was found in known_face_encodings, just use the first one.
                # if True in matches:
                #     first_match_index = matches.index(True)
                #     name = known_face_names[first_match_index]

                # Or instead, use the known face with the smallest distance to the new face
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]

                face_names.append(name)

        process_this_frame = not process_this_frame


        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        # Display the resulting image
        cv2.imshow('Video', frame)

        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()
    
    return redirect('student:my-info')
