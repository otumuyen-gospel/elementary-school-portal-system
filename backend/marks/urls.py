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
    path('class-marks/<int:classId>/', ClassMark.as_view(), name=ClassMark.name),
    path('mark-list/', MarkList.as_view(), name=MarkList.name),
    path('user-marks/<int:userId>/', UserMark.as_view(), name=UserMark.name),
    path('create-marks/', MarkCreate.as_view(), name=MarkCreate.name),
    path('delete-mark/<int:id>/', MarkDelete.as_view(), name=MarkDelete.name),
    path('update-mark/<int:id>/', MarkUpdate.as_view(), name=MarkUpdate.name),
    path('export-marks/', ExportUserMarks.as_view(), name=ExportUserMarks.name),
]
