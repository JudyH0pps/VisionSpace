from .models import File
from django.conf import settings
from rest_framework import serializers

class FileSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField(source='get_file_url')
    
    def get_file_url(self, obj):
        return settings.BACKEND_URL + 'files/' + str(obj.file)[7:]

    class Meta:
        model = File
        fields = "__all__"
