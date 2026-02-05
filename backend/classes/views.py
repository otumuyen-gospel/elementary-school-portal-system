from django.shortcuts import render
from rest_framework import status
from .models import Class
from .serializers import ClassSerializers
from rest_framework import status
from rest_framework.reverse import reverse
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
class ClassList(generics.ListAPIView):
    queryset = Class.objects.all()
    serializer_class = ClassSerializers
    permission_classes = [IsAuthenticated, IsInGroup, ]
    required_groups = ['admin','teacher','parent','student']
    name = 'class-list'

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    #you can filter by field names specified here keyword e.g url?className='primary one'
    filterset_fields = ('className', 'classCode',) 

     #you can search using the "search" keyword
    search_fields = ('className', 'classCode',)

    #you can order using the "ordering" keyword
    ordering_fields = ('className', 'classCode',)

    
#this generic class will handle UPDATE(list 1 item) by admin only 
class ClassUpdate(generics.UpdateAPIView):
    queryset = Class.objects.all()
    serializer_class = ClassSerializers
    permission_classes = [IsAuthenticated,IsInGroup, ]
    required_groups = ['admin',]
    name = 'class-update'
    lookup_field = 'id'


#this generic class will handle DELETE(list 1 item) ONly Admin and teacher
class ClassDelete(generics.DestroyAPIView):
    queryset = Class.objects.all()
    serializer_class = ClassSerializers
    permission_classes = [IsAuthenticated,IsInGroup,]
    required_groups = ['admin',]
    name = 'remove-class'
    lookup_field = 'id'

#this generic class will handle Creation(list 1 item) only admin and teacher
class ClassCreate(generics.CreateAPIView):
    queryset = Class.objects.all()
    serializer_class = ClassSerializers
    permission_classes = [IsAuthenticated,IsInGroup,]
    required_groups = ['admin',]
    name = 'create-class'
    
#this generic class will handle GET(list 1 item) - can be accessed by all user
class UserClass(generics.RetrieveAPIView):
    queryset = Class.objects.all()
    serializer_class = ClassSerializers
    permission_classes = [IsAuthenticated,IsInGroup,]
    required_groups = ['student','parent',]
    name = 'user-class'
    lookup_field = 'id'

    def get_url_values(self):
        url = self.request.build_absolute_uri()
        pathList = urlparse(url).path.split('/')
        if pathList[len(pathList)-1].isspace():
            return  pathList[len(pathList)-2]   #second to last word
        
        return pathList[len(pathList)-2] #last word

    def get_queryset(self):

        # Example: Filter by classId
        val = int(self.get_url_values())
        classId = self.request.user.classId.id
        if (classId != None and val == classId):
            return self.queryset.filter(id=val)
        else:
            raise PermissionDenied("You don't have access right")
   