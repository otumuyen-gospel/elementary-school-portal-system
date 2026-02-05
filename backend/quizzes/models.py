# Create your models here.
from django.db import models
from classes.models import Class
from subjects.models import Subject

# Create your models here.
class Quiz(models.Model):
    question = models.TextField(unique=True,
                                  max_length=1000, 
                                  blank=False, null=False)
    option1 = models.CharField(blank=False, null=False)
    option2 = models.CharField(blank=False, null=False)
    option3 = models.CharField(blank=False, null=False)
    answer = models.CharField(blank=False, null=False)
    classId = models.ForeignKey(Class, on_delete=models.CASCADE)
    subjectId = models.ForeignKey(Subject, on_delete=models.CASCADE)
    setAsQuiz = models.BooleanField(default=False)
    startDate = models.DateField(editable=True)
    endDate = models.DateField(editable=True)
    
    class Meta:
        ordering = ('subjectId','classId')
    def __str__(self):
        return self.question