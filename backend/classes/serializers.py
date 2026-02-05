from rest_framework import serializers
from .models import Class

class ClassSerializers(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = '__all__'