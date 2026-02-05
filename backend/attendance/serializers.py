from rest_framework import serializers
from .models import Attendance

class AttendanceSerializers(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'




class ClassAttendanceSerializer(serializers.Serializer):
    SN = serializers.IntegerField()
    firstName = serializers.CharField()
    lastName = serializers.CharField()
    className  = serializers.CharField()
    attendance = serializers.CharField()
    date = serializers.DateTimeField()
    remark = serializers.CharField()