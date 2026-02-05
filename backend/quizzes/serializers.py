from rest_framework import serializers
from .models import Quiz
from datetime import date

class QuizSerializers(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = '__all__'
    
    #custom method to expire quiz that are due for expiration
    def expireQuizzes():
        quizzes = Quiz.objects.all()
        for quiz in quizzes:
            if quiz.endDate < date.today():
                quiz.setAsQuiz = False
                quiz.save()
        
        