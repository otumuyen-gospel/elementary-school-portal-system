# Create your models here.
from django.db import models
from account.models import User
from subjects.models import Subject
from classes.models import Class


# Create your models here.
class Mark(models.Model):
    examScore = models.CharField(blank=True)
    test_score1 = models.CharField(blank=True)
    test_score2 = models.CharField(blank=True)
    test_score3 = models.CharField(blank=True)

    homework_score1 = models.CharField(blank=True)
    homework_score2 = models.CharField(blank=True)
    homework_score3 = models.CharField(blank=True)

    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    subjectId = models.ForeignKey(Subject, on_delete=models.CASCADE)
    classId  = models.ForeignKey(Class, on_delete=models.CASCADE)
    
    class Meta:
        ordering = ('subjectId','classId',)
    def __str__(self):
        return f"{self.classId}"