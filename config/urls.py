from django.urls import path, include
from . import views
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

app_name = "authentication"

urlpatterns = [
    path("",views.index, name="index"),
    path('admin/', admin.site.urls, name="admin"),
    path("authentication/", include('authentication.urls')),
    path("professor/", include('professor.urls')),
    path("student/", include('student.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)