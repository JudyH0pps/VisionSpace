from rest_framework import serializers
from django.contrib.auth import get_user_model
from accounts.serializers import UserNicknameSerializer, UserNameSerializer
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

class HistoryViewSerializer(serializers.ModelSerializer):
    # session_id = serializers.CharField(source='board_pk.session_id')
    # session_id = serializers.SerializerMethodField(method_name="get_session_id")
    username = serializers.CharField(source='user_pk.username', read_only=True)
    
    # def get_session_id(self, obj):
    #     target_board = Board.objects.get(pk=obj.board_id)
    #     return target_board.session_id

    class Meta:
        model = History
        exclude = ["id", "user_pk", "board_id"]

class BoardViewSerializer(serializers.ModelSerializer):
    user_list = UserNameSerializer(read_only=True, many=True)
    admin_username = serializers.CharField(source='super_admin.username')
    
    class Meta:
        model = Board
        exclude = ["id", "max_tab_index", "super_admin"]

class TabViewSerializer(serializers.ModelSerializer):
    # session_id = serializers.CharField(source='board_pk.session_id')
    
    class Meta:
        model = Tab
        exclude = ["id", "max_note_index", "board_pk"]

class NoteViewSerializer(serializers.ModelSerializer):
    # session_id = serializers.CharField(source='board_pk.session_id')
    tab_index = serializers.IntegerField(source="tab_pk.tab_index")
    type_pk = TypeSerializer(read_only=True)
    username = serializers.CharField(source='user_pk.username', read_only=True)

    class Meta:
        model = Note
        exclude = ["id", "tab_pk", "user_pk", "board_pk"]

# class ArticleSerializer(serializers.ModelSerializer):
#     user = UserSerializer(required=False)  # required=False => is_valid() 에서 유무검증 pass
#     class Meta: 
#         model = Board
#         fields = '__all__'
