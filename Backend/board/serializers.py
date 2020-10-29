from rest_framework import serializers
from accounts.serializers import UserNicknameSerializer
from .models import Board, Tab, Type, Note, History
# from accounts.serializers import UserSerializer

class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = '__all__'

class BoardViewSerializer(serializers.ModelSerializer):
    user_list = UserNicknameSerializer(read_only=True, many=True)
    admin_nickname = serializers.CharField(source='super_admin.nickname')
    
    class Meta:
        model = Board
        exclude = ["id", "max_tab_index", "super_admin"]

class TabSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tab
        fields = '__all__'

class TabViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tab
        exclude = ["id", "max_note_index"]

class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = '__all__'

class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = '__all__'

class NoteViewSerializer(serializers.ModelSerializer):
    tab_index = serializers.IntegerField(source="tab_pk.tab_index")
    type_pk = TypeSerializer(read_only=True)
    nickname = serializers.CharField(source='user_pk.nickname', read_only=True)

    class Meta:
        model = Note
        exclude = ["id", "tab_pk", "user_pk"]

class HistorySerializer(serializers.ModelSerializer):
    nickname = serializers.CharField(source='user_pk.nickname', read_only=True)
    
    class Meta:
        model = History
        exclude = ["id", "user_pk"]

# class ArticleSerializer(serializers.ModelSerializer):
#     user = UserSerializer(required=False)  # required=False => is_valid() 에서 유무검증 pass
#     class Meta: 
#         model = Board
#         fields = '__all__'
