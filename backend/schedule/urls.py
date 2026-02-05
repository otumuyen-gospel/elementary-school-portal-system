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
    path('schedule-list/', ScheduleList.as_view(), name=ScheduleList.name),
    path('create-schedule/', ScheduleCreate.as_view(), name=ScheduleCreate.name),
    path('delete-schedule/<int:id>/', ScheduleDelete.as_view(), name=ScheduleDelete.name),
    path('update-schedule/<int:id>/', ScheduleUpdate.as_view(), name=ScheduleUpdate.name),
]
