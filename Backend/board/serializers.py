from rest_framework import serializers

from .models import Board, Tab, Type, Note, History
# from accounts.serializers import UserSerializer

class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = '__all__'

class TabSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tab
        fields = '__all__'

class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = '__all__'

class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = '__all__'

class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = History
        fields = '__all__'

# class ArticleSerializer(serializers.ModelSerializer):
#     user = UserSerializer(required=False)  # required=False => is_valid() 에서 유무검증 pass
#     class Meta: 
#         model = Board
#         fields = '__all__'
