from rest_framework import serializers
from .models import Complaint

class ComplaintSerializers(serializers.ModelSerializer):
    class Meta:
        model = Complaint
        fields = '__all__'