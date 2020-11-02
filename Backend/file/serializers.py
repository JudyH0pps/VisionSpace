from .models import File
from django.conf import settings
from rest_framework import serializers

class FileSerializer(serializers.ModelSerializer):    
    class Meta:
        model = File
        fields = "__all__"
