from django.db import models

# Create your models here.
class Class(models.Model):
    className = models.CharField(unique=True,
                                  max_length=50, 
                                  blank=False, null=False)
    classCode = models.CharField(unique=True,
                                  max_length=7, 
                                  blank=False, null=False)
    class Meta:
        ordering = ('className',)
    def __str__(self):
        return self.className