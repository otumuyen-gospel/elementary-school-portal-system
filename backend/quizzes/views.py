from django.shortcuts import render
from rest_framework import status
from .models import Quiz
from .serializers import QuizSerializers
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from urllib.parse import urlparse
from rest_framework.permissions import IsAuthenticated, IsAdminUser,AllowAny
from django_filters import AllValuesFilter, DateTimeFilter, NumberFilter
from account.permissions import IsInGroup
from rest_framework.exceptions import PermissionDenied
from  datetime  import date


'''
NOTE: that a global pagination has been set on this generic api 
      classes below you can find the settings in global settings for
      the project under REST_FRAMEWORK dictionaries.
      this pagination settings are working because of the generic
      API class used below it may not work on other API view that
      not from the generic classes. Also added is the django filters
      app for ordering, search and filtering
'''

#this generic class for listing users attendance in a class 
class ClassQuiz(generics.ListAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializers
    permission_classes = [IsAuthenticated, IsInGroup,]
    required_groups = ['admin','teacher',]
    name = 'class-quiz'

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
   #you can filter by field names specified here keyword e.g url?className='primary one'
    filterset_fields = ('subjectId__id','question','option1','option2','option3',
                     'answer',) 

     #you can search using the "search" keyword
    search_fields = ('subjectId__id','question','option1','option2','option3',
                     'answer',) 

    #you can order using the "ordering" keyword
    ordering_fields = ('subjectId__id','question','option1','option2','option3',
                     'answer',)

    def get_url_values(self):
        url = self.request.build_absolute_uri()
        pathList = urlparse(url).path.split('/')
        if pathList[len(pathList)-1].isspace():
            return  pathList[len(pathList)-2]   #second to last word
        
        return pathList[len(pathList)-2] #last word

    def get_queryset(self):
         #expire quizzes that due for expiration
        self.expireQuiz()

        # Example: Filter by classId
        val = int(self.get_url_values())
        userClass = self.request.user.classId
        if (userClass != None and val == userClass.id) or \
        self.request.user.is_superuser:
            return self.queryset.filter(classId=val)
        else:
            raise PermissionDenied("You don't have access right")
    
    def expireQuiz(self):
         if self.queryset.count():
            self.queryset.filter(endDate__lt=date.today()).update(setAsQuiz=False)



#this generic class will handle GET method to be used by the admin alone
class QuizList(generics.ListAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializers
    permission_classes = [IsAuthenticated, IsInGroup, ]
    required_groups = ['admin',]
    name = 'quiz-list'

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    #you can filter by field names specified here keyword e.g url?className='primary one'
    filterset_fields = ('subjectId__id','question','option1','option2','option3',
                     'answer',) 

     #you can search using the "search" keyword
    search_fields = ('subjectId__id','question','option1','option2','option3',
                     'answer',) 

    #you can order using the "ordering" keyword
    ordering_fields = ('subjectId__id','question','option1','option2','option3',
                     'answer',)
    
#this generic class will handle UPDATE(list 1 item) by admin and teacher only 
class QuizUpdate(generics.UpdateAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializers
    permission_classes = [IsAuthenticated,IsInGroup,]
    required_groups = ['admin','teacher']
    name = 'Mark-update'
    lookup_field = 'id'
    def get_object(self):
        obj = super().get_object()
        if self.request.user.is_superuser or \
            obj.classId.id == self.request.user.classId.id:
             return obj
        else:
            raise PermissionDenied("You do not have permission to edit this object.")



#this generic class will handle DELETE(list 1 item) ONly Admin and teacher
class QuizDelete(generics.DestroyAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializers
    permission_classes = [IsAuthenticated,IsInGroup, ]
    required_groups = ['admin','teacher']
    name = 'remove-quiz'
    lookup_field = 'id'
    def get_object(self):
        obj = super().get_object()
        if self.request.user.is_superuser or \
            obj.classId.id == self.request.user.classId.id:
             return obj
        else:
            raise PermissionDenied("You do not have permission to edit this object.")


#this generic class will handle Creation(list 1 item) only admin and teacher
class QuizCreate(generics.CreateAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializers
    permission_classes = [IsAuthenticated,IsInGroup,]
    required_groups = ['admin','teacher']
    name = 'quiz-mark'
    
#this generic class will handle GET(list 1 item) - can be accessed by all user
class UserQuiz(generics.ListAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializers
    permission_classes = [IsAuthenticated,IsInGroup,]
    required_groups = ['student',]
    name = 'user-quiz'

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    #you can filter the class quizzes by their subject Ids'
    filterset_fields = ('subjectId__id',) 

     #you can search using the "search" keyword
    search_fields = ('subjectId__id',)

    #you can order using the "ordering" keyword
    ordering_fields = ('subjectId__id',)

    def get_url_values(self):
        url = self.request.build_absolute_uri()
        pathList = urlparse(url).path.split('/')
        if pathList[len(pathList)-1].isspace():
            return  pathList[len(pathList)-2]   #second to last word
        
        return pathList[len(pathList)-2] #last word

    def get_queryset(self):
        #expire quizzes that due for expiration
        self.expireQuiz()

        # Example: Filter by classId
        val = int(self.get_url_values())
        classId = self.request.user.classId
        if (classId != None and val == classId.id):
            #return only quiz that are set by class teacher and still active as quiz
            return self.queryset.filter(classId=val, setAsQuiz=True)
        else:
            raise PermissionDenied("You don't have access right")
    

    def expireQuiz(self):
         if self.queryset.count():
            self.queryset.filter(endDate__lt=date.today()).update(setAsQuiz=False)