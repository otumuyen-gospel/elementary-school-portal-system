from rest_framework import serializers
from .models import Subject

class SubjectSerializers(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'