from rest_framework import serializers
from django.contrib.auth import get_user_model
from accounts.serializers import UserNicknameSerializer, UserNameSerializer
from .models import Board, Tab, Type, Note, History, Capsule, Time_Machine
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
    username = serializers.CharField(source='user_pk.username', read_only=True)
    
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

class CapsuleViewSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user_pk.username', read_only=True)

    class Meta:
        model = Capsule
        exclude = ["id", "user_pk"]

class TimeMachineViewSerializer(serializers.ModelSerializer):
    capsule_list = CapsuleViewSerializer(many=True, read_only=True)
    
    class Meta:
        model = Time_Machine
        fields = '__all__'
