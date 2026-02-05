"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from .views import *
urlpatterns = [
    path('class-attendance/<int:classId>/', ClassAttendance.as_view(), name=ClassAttendance.name),
    path('attendance-list/', AttendanceList.as_view(), name=AttendanceList.name),
    path('user-attendance/<int:userId>/', UserAttendance.as_view(), name=UserAttendance.name),
    path('create-attendance/', AttendanceCreate.as_view(), name=AttendanceCreate.name),
    path('delete-attendance/<int:id>/', AttendanceDelete.as_view(), name=AttendanceDelete.name),
    path('update-attendance/<int:id>/', AttendanceUpdate.as_view(), name=AttendanceUpdate.name),
    path('export-attendance/', ExportClassAttendance.as_view(), name=ExportClassAttendance.name),
]
