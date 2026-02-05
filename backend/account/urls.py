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
    path('class-users/<int:classId>/', ClassUsers.as_view(), name=ClassUsers.name),
    path('users-list/', UsersList.as_view(), name=UsersList.name),
    path('user-update/<int:id>/', UserUpdate.as_view(), name=UserUpdate.name),
    path('user-promotion/<int:id>/', UserPromotion.as_view(), name=UserPromotion.name),
    path('remove-user/<int:id>/', UserDelete.as_view(), name=UserDelete.name),
    path('retrieve-user/<int:id>/', UserRetrieve.as_view(), name=UserRetrieve.name),
    path('create-user/', UserCreate.as_view(), name=UserCreate.name),
    path('system-backup/', BackupDatabaseAPIView.as_view(), name=BackupDatabaseAPIView.name),
    path('system-restore/', RestoreDatabaseAPIView.as_view(), name=RestoreDatabaseAPIView.name),
    path('export-users/', ExportUsers.as_view(), name=ExportUsers.name),
]
