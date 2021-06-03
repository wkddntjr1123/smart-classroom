from django.urls import path
from . import views

app_name = "student"

urlpatterns = [
    path("my-info/", views.myInfo, name="my-info"),
    path("my-attendance/", views.myAttendance, name="my-attendance"),
    path("change-image/", views.changeImage, name="change-image"),
    path("confirm-attendance/<int:lecture_id>/<int:weekNum>", views.confirmAttendance, name="confirm-attendance"),
    path("enrolment/",views.enrolment, name="enrolment"),
    path("facetest/",views.face_recognization,name="face"),
]
