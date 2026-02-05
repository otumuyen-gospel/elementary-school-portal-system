
# Create your views here.
from django.shortcuts import render
from rest_framework import status
from .models import Homework
from .serializers import HomeworkSerializers
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from urllib.parse import urlparse
from rest_framework.permissions import IsAuthenticated, IsAdminUser,AllowAny
from django_filters import AllValuesFilter, DateTimeFilter, NumberFilter
from account.permissions import IsInGroup
from rest_framework.exceptions import PermissionDenied


'''
NOTE: that a global pagination has been set on this generic api 
      classes below you can find the settings in global settings for
      the project under REST_FRAMEWORK dictionaries.
      this pagination settings are working because of the generic
      API class used below it may not work on other API view that
      not from the generic classes. Also added is the django filters
      app for ordering, search and filtering
'''


#this generic class will handle GET method to be used by the admin alone
class HomeworkList(generics.ListAPIView):
    queryset = Homework.objects.all()
    serializer_class = HomeworkSerializers
    permission_classes = [IsAuthenticated, IsInGroup,]
    required_groups = ['admin',]
    name = 'homework-list'

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    #you can filter by field names specified here keyword e.g url?className='primary one'
    filterset_fields = ('userId__id','title','submission')   

     #you can search using the "search" keyword
    search_fields = ('userId__id','title','submission') 

    #you can order using the "ordering" keyword
    ordering_fields = ('userId__id','title','submission') 

    
class ClassHomework(generics.ListAPIView):
    queryset = Homework.objects.all()
    serializer_class = HomeworkSerializers
    permission_classes = [IsAuthenticated, IsInGroup, ]
    required_groups = ['admin','teacher']
    name = 'class-homework'

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    #you can filter by field names specified here keyword e.g url?className='primary one'
    filterset_fields = ('userId__id','title','submission')  

     #you can search using the "search" keyword
    search_fields = ('userId__id','title','submission') 

    #you can order using the "ordering" keyword
    ordering_fields = ('userId__id','title','submission') 

    def get_url_values(self):
        url = self.request.build_absolute_uri()
        pathList = urlparse(url).path.split('/')
        if pathList[len(pathList)-1].isspace():
            return  pathList[len(pathList)-2]   #second to last word
        
        return pathList[len(pathList)-2] #last word

    def get_queryset(self):

        # Example: Filter by classId
        val = int(self.get_url_values())
        userClass = self.request.user.classId
        if (userClass != None and val == userClass.id) or \
        self.request.user.is_superuser:
            return self.queryset.filter(classId=val)
        else:
            raise PermissionDenied("You don't have access right")


#this generic class will handle UPDATE(list 1 item) by admin only 
class HomeworkUpdate(generics.UpdateAPIView):
    queryset = Homework.objects.all()
    serializer_class = HomeworkSerializers
    permission_classes = [IsAuthenticated, IsInGroup,]
    required_groups = ['admin', 'student']
    name = 'homework-update'
    lookup_field = 'id'
    def get_object(self):
        obj = super().get_object()
        if self.request.user.is_superuser or \
            obj.userId.id == self.request.user.id:
             return obj
        else:
            raise PermissionDenied("You do not have permission to edit this object.")




#this generic class will handle DELETE(list 1 item) ONly Admin and teacher
class HomeworkDelete(generics.DestroyAPIView):
    queryset = Homework.objects.all()
    serializer_class = HomeworkSerializers
    permission_classes = [IsAuthenticated,IsInGroup,]
    required_groups = ['admin','student']
    name = 'remove-homework'
    lookup_field = 'id'
    def get_object(self):
        obj = super().get_object()
        if self.request.user.is_superuser or \
            obj.userId.id == self.request.user.id:
             return obj
        else:
            raise PermissionDenied("You do not have permission to edit this object.")
        
#this generic class will handle Creation(list 1 item) only admin and teacher
class HomeworkCreate(generics.CreateAPIView):
    queryset = Homework.objects.all()
    serializer_class = HomeworkSerializers
    permission_classes = [IsAuthenticated,IsInGroup,]
    required_groups = ['admin','student',]
    name = 'create-homework'
    
#this generic class will handle GET(list 1 item) - can be accessed by all user
class UserHomework(generics.ListAPIView):
    queryset = Homework.objects.all()
    serializer_class = HomeworkSerializers
    permission_classes = [IsAuthenticated,IsInGroup,]
    required_groups = ['student','admin']
    name = 'user-homework'

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    #you can filter by field names specified here keyword e.g url?className='primary one'
    filterset_fields = ('userId__id','title','submission') 

     #you can search using the "search" keyword
    search_fields = ('userId__id','title','submission') 

    #you can order using the "ordering" keyword
    ordering_fields = ('userId__id','title','submission') 

    def get_url_values(self):
        url = self.request.build_absolute_uri()
        pathList = urlparse(url).path.split('/')
        if pathList[len(pathList)-1].isspace():
            return  pathList[len(pathList)-2]   #second to last word
        
        return pathList[len(pathList)-2] #last word

    def get_queryset(self):

        # Example: Filter by classId
        val = int(self.get_url_values())
        id = self.request.user.id
        if (id != None and val == id) or \
        self.request.user.is_superuser:
            return self.queryset.filter(userId=val)
        else:
            raise PermissionDenied("You don't have access right")