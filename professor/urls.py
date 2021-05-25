from django.urls import path
from . import views

app_name = "professor"

urlpatterns = [
    path("manage-attendance/", views.manageAttendance, name="manage-attendance"),
]
