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
    path('complaint-list/', ComplaintList.as_view(), name=ComplaintList.name),
    path('class-complaint-list/<int:classId>/', ClassComplaint.as_view(), name=ClassComplaint.name),
    path('user-complaint-list/<int:userId>/', UserComplaint.as_view(), name=UserComplaint.name),
    path('create-complaint/', ComplaintCreate.as_view(), name=ComplaintCreate.name),
    path('delete-complaint/<int:id>/', ComplaintDelete.as_view(), name=ComplaintDelete.name),
    path('update-complaint/<int:id>/', ComplaintUpdate.as_view(), name=ComplaintUpdate.name),
]
