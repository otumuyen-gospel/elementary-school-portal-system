# Create your models here.
from django.db import models
from classes.models import Class

# Create your models here.
class Subject(models.Model):
    subjectName = models.CharField(max_length=100, 
                                  blank=False, null=False)
    subjectCode = models.CharField(max_length=7, 
                                  blank=False, null=False)
    classId = models.ForeignKey(Class, on_delete=models.CASCADE)

    TERM_ONE = 'First Term'
    TERM_TWO = 'Second Term'
    TERM_THREE = 'Third Term'
    SUBJECT_TERM = [
        (TERM_ONE,'First Term'),
        (TERM_TWO,'Second Term'),
        (TERM_THREE,'Third Term'),
    ]
    term = models.CharField(choices=SUBJECT_TERM,
                               default=TERM_ONE)
    
    class Meta:
        ordering = ('subjectName',)
    def __str__(self):
        return self.subjectName