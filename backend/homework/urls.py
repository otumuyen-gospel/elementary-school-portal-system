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
    path('homework-list/', HomeworkList.as_view(), name=HomeworkList.name),
    path('class-homework-list/<int:classId>/', ClassHomework.as_view(), name=ClassHomework.name),
    path('user-homework-list/<int:userId>/', UserHomework.as_view(), name=UserHomework.name),
    path('create-homework/', HomeworkCreate.as_view(), name=HomeworkCreate.name),
    path('delete-homework/<int:id>/', HomeworkDelete.as_view(), name=HomeworkDelete.name),
    path('update-homework/<int:id>/', HomeworkUpdate.as_view(), name=HomeworkUpdate.name),
]
