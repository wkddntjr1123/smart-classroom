from django.urls import path
from . import views

app_name = "professor"

urlpatterns = [
    path("manage-attendance/<int:lecture_id>/<int:weekNum>", views.manageAttendance, name="manage-attendance"),
    path("manage-lecture/", views.manageLecture, name="manage-lecture"),
    path("create-lecture/", views.createLecture, name="create-lecture"),
    
]
