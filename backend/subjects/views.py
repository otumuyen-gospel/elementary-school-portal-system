from django.shortcuts import render
from rest_framework import status
from .models import Subject
from .serializers import SubjectSerializers
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

class ClassSubjectsList(generics.ListAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializers
    permission_classes = [IsAuthenticated, IsInGroup,]
    required_groups = ['admin','teacher','student','parent']
    name = 'class-subject-list'

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    #you can filter by field names specified here keyword e.g url?className='primary one'
    filterset_fields = ('subjectName','subjectCode','classId__id',) 

     #you can search using the "search" keyword
    search_fields = ('subjectName','subjectCode','classId__id',) 

    #you can order using the "ordering" keyword
    ordering_fields = ('subjectName','subjectCode','classId__id',) 

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

    
#this generic class will handle UPDATE(list 1 item) by admin and teacher only 
class SubjectUpdate(generics.UpdateAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializers
    permission_classes = [IsAuthenticated,IsInGroup,]
    required_groups = ['admin',]
    name = 'subject-update'
    lookup_field = 'id'

#this generic class will handle DELETE(list 1 item) ONly Admin and teacher
class SubjectDelete(generics.DestroyAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializers
    permission_classes = [IsAuthenticated,IsInGroup,]
    required_groups = ['admin',]
    name = 'remove-subject'
    lookup_field = 'id'
    

#this generic class will handle Creation(list 1 item) only admin and teacher
class SubjectCreate(generics.CreateAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializers
    permission_classes = [IsAuthenticated,IsInGroup,]
    required_groups = ['admin',]
    name = 'subject-create'
 
class SubjectList(generics.ListAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializers
    permission_classes = [IsAuthenticated, IsInGroup,]
    required_groups = ['admin','teacher','student','parent']
    name = 'subject-list'

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    #you can filter by field names specified here keyword e.g url?className='primary one'
    filterset_fields = ('subjectName','subjectCode','classId__id',) 

     #you can search using the "search" keyword
    search_fields = ('subjectName','subjectCode','classId__id',) 

    #you can order using the "ordering" keyword
    ordering_fields = ('subjectName','subjectCode','classId__id',) 