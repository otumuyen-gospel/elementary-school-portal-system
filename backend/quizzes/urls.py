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
    path('class-quiz/<int:classId>/', ClassQuiz.as_view(), name=ClassQuiz.name),
    path('quiz-list/', QuizList.as_view(), name=QuizList.name),
    path('user-quiz/<int:classId>/', UserQuiz.as_view(), name=UserQuiz.name),
    path('create-quiz/', QuizCreate.as_view(), name=QuizCreate.name),
    path('delete-quiz/<int:id>/', QuizDelete.as_view(), name=QuizDelete.name),
    path('update-quiz/<int:id>/', QuizUpdate.as_view(), name=QuizUpdate.name),
]
