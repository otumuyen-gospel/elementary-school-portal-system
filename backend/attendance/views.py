from .models import Attendance
from .serializers import AttendanceSerializers
from django.shortcuts import render
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
from django.http import HttpResponse
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font
from io import BytesIO
from account.models import User
from classes.models import Class
from subjects.models import Subject
from .serializers import ClassAttendanceSerializer
from rest_framework.views import APIView


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
class ClassAttendance(generics.ListAPIView):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializers
    permission_classes = [IsAuthenticated, IsInGroup,]
    required_groups = ['admin','teacher']
    name = 'class-attendance'

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    #you can filter by field names specified here keyword e.g url?className='primary one'
    filterset_fields = ('userId__firstName','date','userId__lastName',
                       'classId__className','classId__classCode','remark','attendance', ) 

     #you can search using the "search" keyword
    search_fields = ('userId__firstName','date','userId__lastName',
                       'classId__className','classId__classCode','remark','attendance',) 

    #you can order using the "ordering" keyword
    ordering_fields = ('userId__firstName','date','userId__lastName',
                       'classId__className','classId__classCode','remark','attendance',) 

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
    

#this generic class will handle GET method to be used by the admin alone
class AttendanceList(generics.ListAPIView):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializers
    permission_classes = [IsAuthenticated, IsInGroup,]
    required_groups = ['admin','teacher','student','parent']
    name = 'attendance-list'

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    #you can filter by field names specified here keyword e.g url?className='primary one'
    filterset_fields = ('userId__firstName','date','userId__lastName',
                       'classId__className','classId__classCode','remark','attendance',) 

     #you can search using the "search" keyword
    search_fields = ('userId__firstName','date','userId__lastName',
                       'classId__className','classId__classCode','remark','attendance',) 

    #you can order using the "ordering" keyword
    ordering_fields = ('userId__firstName','date','userId__lastName',
                       'classId__className','classId__classCode','remark','attendance',) 

    
#this generic class will handle UPDATE(list 1 item) by admin and teacher only 
class AttendanceUpdate(generics.UpdateAPIView):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializers
    permission_classes = [IsAuthenticated,IsInGroup,]
    required_groups = ['admin','teacher']
    name = 'attendance-update'
    lookup_field = 'id'
    def get_object(self):
        obj = super().get_object()
        if self.request.user.is_superuser or \
            obj.classId.id == self.request.user.classId.id:
             return obj
        else:
            raise PermissionDenied("You do not have permission to edit this object.")


#this generic class will handle DELETE(list 1 item) ONly Admin and teacher
class AttendanceDelete(generics.DestroyAPIView):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializers
    permission_classes = [IsAuthenticated,IsInGroup,]
    required_groups = ['admin','teacher']
    name = 'remove-attendance'
    lookup_field = 'id'
    def get_object(self):
        obj = super().get_object()
        if self.request.user.is_superuser or \
            obj.classId.id == self.request.user.classId.id:
             return obj
        else:
            raise PermissionDenied("You do not have permission to edit this object.")

#this generic class will handle Creation(list 1 item) only admin and teacher
class AttendanceCreate(generics.CreateAPIView):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializers
    permission_classes = [IsAuthenticated,IsInGroup,]
    required_groups = ['admin','teacher']
    name = 'create-attendance'
    
#this generic class will handle GET(list 1 item) - can be accessed by all user
class UserAttendance(generics.ListAPIView):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializers
    permission_classes = [IsAuthenticated,IsInGroup,]
    required_groups = ['student','parent']
    name = 'user-attendance'

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    #you can filter by field names specified here keyword e.g url?className='primary one'
    filterset_fields = ('userId__firstName','date','userId__lastName',
                       'classId__className','classId__classCode','remark','attendance') 

     #you can search using the "search" keyword
    search_fields = ('userId__firstName','date','userId__lastName',
                       'classId__className','classId__classCode','remark','attendance',) 

    #you can order using the "ordering" keyword
    ordering_fields = ('userId__firstName','date','userId__lastName',
                       'classId__className','classId__classCode','remark','attendance',) 

    def get_url_values(self):
        url = self.request.build_absolute_uri()
        pathList = urlparse(url).path.split('/')
        if pathList[len(pathList)-1].isspace():
            return  pathList[len(pathList)-2]   #second to last word
        
        return pathList[len(pathList)-2] #last word

    def get_queryset(self):

        val = int(self.get_url_values())
        userId = self.request.user.id
        childId = self.request.user.childId
        if userId != None and val == userId: #student
          return self.queryset.filter(userId=val)
        elif childId != None and val == int(childId): # parent
            return self.queryset.filter(userId=childId)
        else:
            raise PermissionDenied("You don't have access right")



#export users to excel
class ExportClassAttendance(APIView):
    permission_classes = [IsAuthenticated,IsInGroup,]
    required_groups = ['teacher',]
    name = 'export'
    def get(self, request, *args, **kwargs): 
        queryset = Attendance.objects.filter(classId=self.request.user.classId.id)
        queryset = self.getData(queryset)
        # 2. Serialize the data (optional but good practice)
        serializer = ClassAttendanceSerializer(data=queryset, many=True)
        try: 
              data = serializer.initial_data
              if serializer.is_valid():
                 data = serializer.data
              # 3. Create an Excel workbook
              wb = Workbook()
              ws = wb.active
              ws.title = "Class Attendance"
              # Add headers (using serializer field names or custom names)
              headers =  [
                 'SN','FirstName','LastName', 'ClassName','Attendance','Date',
                 'Remark',
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
              response['Content-Disposition'] = 'attachment; filename="class_attendance.xlsx"'
              return response
        except Exception as e:
            return Response({"error": str(e)}, status=500)
    def getData(self,queryset):
         data = []
         count = 1
         for obj in queryset:
             cl = Class.objects.get(id=obj.classId.id)
             user = User.objects.get(pk=obj.userId.id)
             attendance = ""
             if obj.attendance:
                 attendance = "\N{check mark}"
             
             newObj = {
                 'SN':count,'FirstName':user.firstName,
                 'LastName':user.lastName, 'ClassName': cl.className,
                 'Attendance': attendance,'Date': obj.date.replace(tzinfo=None),
                 'Remark': obj.remark,
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