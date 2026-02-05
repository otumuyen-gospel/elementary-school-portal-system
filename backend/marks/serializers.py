from rest_framework import serializers
from .models import Mark

class MarkSerializers(serializers.ModelSerializer):
    class Meta:
        model = Mark
        fields = '__all__'



class ExportMarks(serializers.Serializer):
    SN = serializers.IntegerField()
    examScore = serializers.CharField()
    test_score1 = serializers.CharField()
    test_score2 = serializers.CharField()
    test_score3 = serializers.CharField()
    homework_score1 = serializers.CharField()
    homework_score2 = serializers.CharField()
    homework_score3 = serializers.CharField()
    firstName = serializers.CharField()
    lastName = serializers.CharField()
    subjectName = serializers.CharField()
    className  = serializers.CharField()