
from django.shortcuts import render
from rest_framework import status
from .models import User
from .serializers import UserSerializers
from rest_framework.reverse import reverse
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from urllib.parse import urlparse
from rest_framework.permissions import IsAuthenticated, IsAdminUser,AllowAny
from django_filters import AllValuesFilter, DateTimeFilter, NumberFilter
from .permissions import IsInGroup
from rest_framework.exceptions import PermissionDenied
from django.contrib.auth.models import Group
from rest_framework.views import APIView
from classes.models import Class
from datetime import datetime
import uuid
from django.core.management import call_command
from django.conf import settings 
from django.http import HttpResponse
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font
from io import BytesIO, StringIO
from .serializers import UserSerializers
from .models import User
from classes.models import Class
from .serializers import ExportUsers


'''
NOTE: that a global pagination has been set on this generic api 
      classes below you can find the settings in global settings for
      the project under REST_FRAMEWORK dictionaries.
      this pagination settings are working because of the generic
      API class used below it may not work on other API view that
      not from the generic classes. Also added is the django filters
      app for ordering, search and filtering
'''

#this generic class for listing users in a class 
class ClassUsers(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializers
    permission_classes = [IsAuthenticated, IsInGroup,]
    required_groups = ['admin','teacher','parent','student']
    name = 'class-users'

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    #you can filter by field names specified here keyword e.g url?className='primary one'
    filterset_fields = ('id','childId','classId__id', 'entrance',
                     'firstName','lastName','email','gender','role') 

     #you can search using the "search" keyword
    search_fields = ('id','childId','classId__id','entrance',
                     'firstName','lastName','email','gender','role') 

    #you can order using the "ordering" keyword
    ordering_fields = ('id','childId','classId__id','entrance',
                     'firstName','lastName','email','gender','role')  


    def get_url_values(self):
        url = self.request.build_absolute_uri()
        pathList = urlparse(url).path.split('/')
        if pathList[len(pathList)-1].isspace():
            return  pathList[len(pathList)-2]   #second to last word
        
        return pathList[len(pathList)-2] #last word

    def get_queryset(self):

        # Example: Filter by classId
        val = int(self.get_url_values())
        if (val):
            return self.queryset.filter(classId=val)
        else:
            raise PermissionDenied("You don't have access right")
        
    

#this generic class will handle GET method to be used by the admin alone
class UsersList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializers
    permission_classes = [IsAuthenticated, IsInGroup,]
    required_groups = ['admin','teacher','parent','student']
    name = 'users-list'

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    #you can filter by field names specified here keyword e.g url?className='primary one'
    filterset_fields = ('id','childId','classId__id','entrance',
                     'firstName','lastName','email','gender','role') 

     #you can search using the "search" keyword
    search_fields = ('id','childId','classId__id','entrance',
                     'firstName','lastName','email','gender','role') 

    #you can order using the "ordering" keyword
    ordering_fields = ('id','childId','classId__id','entrance',
                     'firstName','lastName','email','gender','role')  

    
#this generic class will handle UPDATE(list 1 item) by users for their account alone
class UserUpdate(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializers
    permission_classes = [IsAuthenticated,IsInGroup,]
    required_groups = ['admin','teacher','student','parent']
    name = 'user-update'
    lookup_field = 'id'
    def get_object(self):
        obj = super().get_object()
        if self.request.user.is_superuser or \
            obj == self.request.user:
             self.updateUserGroup(obj)
             return obj
        else:
            raise PermissionDenied("You do not have permission to edit this object.")
    
    def updateUserGroup(self,obj):
        user = self.queryset.get(pk=obj.id)
        if self.request.data['role'] != user.role: #user changed role so update role
            group = Group.objects.get(name=user.role)
            new_group = Group.objects.get(name=self.request.data['role'])
            if group in user.groups.all():
              user.groups.remove(group)
              user.groups.add(new_group)


#this generic class will handle DELETE(list 1 item) ONly Admin
class UserDelete(generics.DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializers
    permission_classes = [IsAuthenticated,IsInGroup,]
    required_groups = ['admin',]
    name = 'remove-user'
    lookup_field = 'id'

#this generic class will handle Creation(list 1 item) only admin
class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializers
    permission_classes = [IsAuthenticated,IsInGroup,]
    required_groups = ['admin',]
    name = 'create-user'
    
#this generic class will handle GET(list 1 item)
class UserRetrieve(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializers
    permission_classes = [IsAuthenticated,IsInGroup,]
    required_groups = ['admin','teacher','student','parent']
    name = 'retrieve-user'
    lookup_field = 'id'
    def get_object(self):
        
        obj = super().get_object()
        if self.request.user.is_superuser:
             return obj
        elif obj == self.request.user:
             return obj
        elif int(obj.id) == int(self.request.user.childId):
             return obj
        else:
            raise PermissionDenied("You do not have permission to view this object.")

'''
 to update only the classId of the user
  1. call the endpoint to this userId with a patch http method to update a single column
  2. and set only classId in your json data to the new classId
  3. e.g set your json:{'classId':newClassId}
  4. and call /endpointUrl/userId/
'''
class UserPromotion(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializers
    permission_classes = [IsAuthenticated,IsInGroup,]
    required_groups = ['admin','teacher',]
    name = 'user-promotion'
    lookup_field = 'id'
    def get_object(self):
        obj = super().get_object()
        if self.request.user.is_superuser or \
            obj.classId.id == self.request.user.classId.id:
             return obj
        else:
            raise PermissionDenied("You do not have permission to edit this object.")


# API for issuing command prompt to the server or os
class BackupDatabaseAPIView(APIView):
    permission_classes = [IsAuthenticated,IsInGroup,]
    required_groups = ['admin',]
    name = 'backup'
    def post(self, request):
        try:
            call_command('dbbackup')  # db backup
            call_command('mediabackup')  # file and media backups
            return Response({"message": "backup initiated successfully.", 
                             'location':settings.STORAGES['dbbackup']['OPTIONS']['location']})
        except Exception as e:
            return Response({"error": str(e)}, status=500)
        

# API for issuing command prompt to the server or os
class RestoreDatabaseAPIView(APIView):
    permission_classes = [IsAuthenticated,IsInGroup,]
    required_groups = ['admin',]
    name = 'restore'
    def post(self, request):
        try:
            call_command('dbrestore','--noinput')  # db restore
            call_command('mediarestore','--noinput')  # file and media restore
            return Response({"message": "restore initiated successfully.",
                            'location':settings.STORAGES['dbbackup']['OPTIONS']['location']})
        except Exception as e:
            return Response({"error": str(e)}, status=500)
         

#export users to excel
class ExportUsers(APIView):
    permission_classes = [IsAuthenticated,IsInGroup,]
    required_groups = ['admin',]
    name = 'export'
    def get(self, request, *args, **kwargs):
        queryset = User.objects.exclude(role='admin') 
        queryset = self.getData(queryset)
        # 2. Serialize the data (optional but good practice)
        serializer = ExportUsers(data=queryset, many=True)
        data = serializer.data
        # 3. Create an Excel workbook
        wb = Workbook()
        ws = wb.active
        ws.title = "User Search Results"
        # Add headers (using serializer field names or custom names)
        headers =  [
                 'SN','Username','FirstName','LastName','Email','Role','ClassName','Dob',
                 'Telephone', 'Gender','Address','Nationality','State',
        ]
        ws.append(headers)
        # Add data rows
        for item in data:
            row_values = [item.get(header) for header in headers] # Or customize based on item keys
            ws.append(row_values)
        #add styles
        self.addStyles(ws)
        self.adjustWidth(ws)
        # 4. Save the workbook to a BytesIO buffer
        excel_buffer = BytesIO()
        wb.save(excel_buffer)
        excel_buffer.seek(0) # Rewind the buffer to the beginning
        # 5. Create an HttpResponse with appropriate headers
        response = HttpResponse(
            excel_buffer.getvalue(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename="User_search_results.xlsx"'
        return response
    def getData(self,queryset):
         data = []
         count = 1
         for obj in queryset:
             cl = Class.objects.get(id=obj.classId.id)
             newObj = {
                 'SN':count,'Username': obj.username, 'FirstName':obj.firstName,
                 'LastName':obj.lastName, 'Email': obj.email,'Role': obj.role,
                 'ClassName': cl.className,'Dob': obj.dob,'Telephone': obj.telephone,
                 'Gender': obj.gender,'Address': obj.address,'Nationality': obj.nationality,
                 'State': obj.state,
             }
             data.append(newObj)
             count = count + 1
         return data
    def addStyles(self, ws):
        bold_font = Font(bold=True)
        for row in ws.iter_rows():
          for cell in row:
           cell.alignment = Alignment(wrap_text=True)
           # Assign the bold_font object to the cell's font attribute
           cell.font = bold_font
    def adjustWidth(self,ws):
        # Iterate over all columns to adjust their widths
        for col in ws.columns:
          max_length = 0
          column_letter = col[0].column_letter # Get the column letter (e.g., 'A', 'B')
          for cell in col:
            try:
            # Check the length of the cell's value
               if len(str(cell.value)) > max_length:
                max_length = len(str(cell.value))
            except TypeError: # Handle cases where cell.value might be None
              pass
            # Calculate adjusted width (add a small buffer for visual spacing)
            adjusted_width = (max_length + 2)
            # Set the column width
            ws.column_dimensions[column_letter].width = adjusted_width

    