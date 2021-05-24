from django.urls import path, include
from . import views
from django.contrib import admin

app_name = "authentication"

urlpatterns = [
    path("",views.index),
    path('admin/', admin.site.urls, name="admin"),
    path("authentication/", include('authentication.urls')),
]
