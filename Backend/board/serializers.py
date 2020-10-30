from rest_framework import serializers
from accounts.serializers import UserNicknameSerializer
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
    session_id = serializers.CharField(source='board_pk.session_id')
    nickname = serializers.CharField(source='user_pk.nickname', read_only=True)
    
    class Meta:
        model = History
        exclude = ["id", "user_pk", "board_pk"]

class BoardViewSerializer(serializers.ModelSerializer):
    user_list = UserNicknameSerializer(read_only=True, many=True)
    admin_nickname = serializers.CharField(source='super_admin.nickname')
    
    class Meta:
        model = Board
        exclude = ["id", "max_tab_index", "super_admin"]

class TabViewSerializer(serializers.ModelSerializer):
    session_id = serializers.CharField(source='board_pk.session_id')
    
    class Meta:
        model = Tab
        exclude = ["id", "max_note_index", "board_pk"]

class NoteViewSerializer(serializers.ModelSerializer):
    session_id = serializers.CharField(source='board_pk.session_id')
    tab_index = serializers.IntegerField(source="tab_pk.tab_index")
    type_pk = TypeSerializer(read_only=True)
    nickname = serializers.CharField(source='user_pk.nickname', read_only=True)

    class Meta:
        model = Note
        exclude = ["id", "tab_pk", "user_pk", "board_pk"]

# class ArticleSerializer(serializers.ModelSerializer):
#     user = UserSerializer(required=False)  # required=False => is_valid() 에서 유무검증 pass
#     class Meta: 
#         model = Board
#         fields = '__all__'
