from django.shortcuts import render

# Create your views here.

def manageAttendance(request) :
    return render(request,"professor/manage-attendance.html")