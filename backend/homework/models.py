# Create your models here.
from django.db import models
from account.models import User
from account.models import Class

# Create your models here.
def upload_to(instance, filename):
    return 'user_homework_{0}_{1}'.format(instance.userId, filename)

class Homework(models.Model):
    title = models.CharField(blank=False)
    link = models.FileField(blank=False, upload_to=upload_to)
    submission = models.DateTimeField(auto_now_add=True, blank=True)
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    classId  = models.ForeignKey(Class, on_delete=models.CASCADE)
    class Meta:
        ordering = ('title','classId',)
    def __str__(self):
        return f"{self.title}"