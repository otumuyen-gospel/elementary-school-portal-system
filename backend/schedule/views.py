
from django.shortcuts import render
from rest_framework import status
from .models import Schedule
from .serializers import ScheduleSerializers
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from urllib.parse import urlparse
from rest_framework.permissions import IsAuthenticated, IsAdminUser,AllowAny
from django_filters import AllValuesFilter, DateTimeFilter, NumberFilter
from account.permissions import IsInGroup
from rest_framework.exceptions import PermissionDenied
from django.utils import timezone


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
class ScheduleList(generics.ListAPIView):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializers
    permission_classes = [IsAuthenticated, IsInGroup,]
    required_groups = ['admin','teacher','student','parent']
    name = 'schedule-list'

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    #you can filter by field names specified here keyword e.g url?className='primary one'
    filterset_fields = ('userId__id','userId__username','classId__classCode',
                        'classId__className','title','detail','startDateTime',) 

     #you can search using the "search" keyword
    search_fields =  ('userId__id','userId__username','classId__classCode',
                        'classId__className','title','detail','startDateTime',)

    #you can order using the "ordering" keyword
    ordering_fields = ('userId__id','userId__username','classId__classCode',
                        'classId__className','title','detail','startDateTime',)

    def get_queryset(self):
        #delete schedules that are due for expiration
        self.deleteSchedules()
        return  self.queryset

    def deleteSchedules(self):
        if self.queryset.count():
            self.queryset.filter(endDateTime__lt=timezone.now()).delete()
    
#this generic class will handle UPDATE(list 1 item) by admin and teacher only 
class ScheduleUpdate(generics.UpdateAPIView):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializers
    permission_classes = [IsAuthenticated,IsInGroup,]
    required_groups = ['admin','teacher']
    name = 'schedule-update'
    lookup_field = 'id'
    def get_object(self):
        obj = super().get_object()
        if self.request.user.is_superuser or \
            obj.userId.id == self.request.user.pk:
             return obj
        else:
            raise PermissionDenied("You do not have permission to edit this object.")


#this generic class will handle DELETE(list 1 item) ONly Admin and teacher
class ScheduleDelete(generics.DestroyAPIView):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializers
    permission_classes = [IsAuthenticated,IsInGroup,]
    required_groups = ['admin','teacher']
    name = 'remove-schedule'
    lookup_field = 'id'
    def get_object(self):
        obj = super().get_object()
        if self.request.user.is_superuser or \
            obj.userId.id == self.request.user.pk:
             return obj
        else:
            raise PermissionDenied("You do not have permission to edit this object.")


#this generic class will handle Creation(list 1 item) only admin and teacher
class ScheduleCreate(generics.CreateAPIView):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializers
    permission_classes = [IsAuthenticated,IsInGroup,]
    required_groups = ['admin','teacher']
    name = 'schedule-create'
 