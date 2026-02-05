import uuid
from django.contrib.auth.models import (AbstractBaseUser, 
BaseUserManager, PermissionsMixin)
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.http import Http404
import random 
from datetime import timedelta
from django.utils import timezone
from .usermanager import AccountManager
from classes.models import Class


def upload_to(instance, filename):
    return 'user_account_{0}_{1}'.format(instance.pk, filename)

class User(AbstractBaseUser, PermissionsMixin):
    pics = models.FileField(blank=True, null=True, upload_to=upload_to)
    email = models.EmailField(db_index=True, unique=True)
    username = models.CharField(max_length=11, unique=True)
    firstName = models.CharField(max_length=255, blank=False)
    lastName = models.CharField(max_length=255, blank=False)
    is_active = models.BooleanField(default=True)
    '''for administrators only'''
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    '''this fields must be entered or unique'''
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email','firstName','lastName','role','gender','is_staff','is_active',
                       'is_superuser']
    GENDER_MALE = 'M'
    GENDER_FEMALE = 'F'
    GENDER_OTHERS = 'O'
    USERS_GENDER = [
        (GENDER_MALE,'male'),
        (GENDER_FEMALE, 'female'),
        (GENDER_OTHERS, 'others'),
    ]
    gender = models.CharField(choices=USERS_GENDER,
                               default=GENDER_MALE)
    ROLE_TEACHER = 'teacher'
    ROLE_ADMIN = 'admin'
    ROLE_PARENT = 'parent'
    ROLE_STUDENT = 'student'
    USERS_ROLES= [
         (ROLE_TEACHER,'teacher'),
         (ROLE_ADMIN,'admin'),
         (ROLE_STUDENT,'student'),
         (ROLE_PARENT,'parent'),
    ]
    role = models.CharField(choices=USERS_ROLES,
                               default=ROLE_STUDENT)
    entrance = models.DateTimeField(blank=True, null=True, default=None)
    dob = models.DateField(blank=True, null=True, default=None)
    classId = models.ForeignKey(Class, on_delete=models.SET_NULL, blank=True, null=True)
    childId = models.CharField(max_length=255, blank=True, null=True, default=None)
    address = models.CharField(max_length=400, blank=True, null=True, default=None)
    nationality = models.CharField(max_length=255 , blank=True, null=True, default=None)
    state = models.CharField(max_length=255, blank=True, null=True, default=None)
    zipCode = models.CharField(max_length=6, blank=True, null=True, default=None)
    telephone = models.CharField(max_length=15, blank=True, null=True, default=None)

    otp = models.CharField(max_length=6, blank=True, null=True, default=None)
    otp_exp = models.DateTimeField(blank=True, null=True, default=None) 
    otp_verified = models.BooleanField(default=False)

    objects = AccountManager()
    class Meta:
        ordering = ('firstName','lastName',)
    def generate_otp(self):
        self.otp = str(random.randint(100000, 999999))  # Generate 6-digit OTP
        self.otp_exp = timezone.now() + timedelta(minutes=10)
        self.otp_verified = False
        self.save()
    def __str__(self):
        return f"{self.firstName} {self.lastName}"
    @property
    def name(self):
        return f"{self.firstName} {self.lastName}"
    