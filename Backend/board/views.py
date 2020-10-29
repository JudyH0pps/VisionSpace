from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Board, Tab, Type, Note, History, User_Board
from .serializers import BoardSerializer, TabSerializer, TypeSerializer, NoteSerializer, HistorySerializer

# Create your views here.
from rest_framework import mixins
from rest_framework.generics import GenericAPIView
from rest_framework import status

from django.db.models import Q

def add_history(user, board, tab, note):
    new_history = History()
    new_history.user_pk = user
    new_history.board_id = board.pk
    new_history.tab_index = tab.tab_index
    new_history.note_index = note.note_index
    new_history.x = note.x
    new_history.y = note.y
    new_history.z = note.z
    new_history.width = note.width
    new_history.height = note.height
    new_history.content = note.content
    new_history.save()
    return

class BoardView(mixins.CreateModelMixin, 
                    mixins.ListModelMixin,
                    GenericAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    lookup_field = 'session_id'

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        create_request = self.create(request, *args, **kwargs)
        created_board = Board.objects.get(pk=create_request.data['id'])
        new_member = User_Board()
        new_member.board_pk = created_board
        new_member.user_pk = request.user
        new_member.is_admin = True
        new_member.save()
        return Response(create_request.data)

class BoardDetailView(mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.DestroyModelMixin,
                        GenericAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    lookup_field = 'session_id'

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

class BoardJoinView(GenericAPIView):
    permission_classes = (IsAuthenticated, )
    def post(self, request, *args, **kwargs):
        target_board = Board.objects.get(session_id=kwargs['session_id'])
        user_search = User_Board.objects.filter(board_pk_id=target_board, user_pk_id=request.user)
        if user_search:
            return Response({
                "status": "303"
            }, status=303)

        new_member = User_Board()
        new_member.board_pk = target_board
        new_member.user_pk = request.user
        new_member.is_admin = False
        new_member.save()
        return Response({
            "status": "200"
        }, status=status.HTTP_200_OK)

class TabView(GenericAPIView):
    serializer_class = TabSerializer
    permission_classes = (IsAuthenticated, )
    def get(self, request, *args, **kwargs):
        target_board = Board.objects.get(pk=kwargs['pk'])
        tab_list = Tab.objects.filter(board_pk_id=target_board)
        resp = TabSerializer(tab_list, many=True)
        return Response(resp.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        target_board = Board.objects.get(pk=kwargs['pk'])
        target_board.max_tab_index += 1
        target_board.save()

        new_tab = Tab()       
        new_tab.board_pk = target_board
        new_tab.tab_index = target_board.max_tab_index
        new_tab.name = request.data["name"]
        new_tab.save()

        resp = TabSerializer(new_tab)
        return Response(
            resp.data, status=status.HTTP_201_CREATED
        )

class TabDetailView(GenericAPIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request, *args, **kwargs):
        target_tab = Tab.objects.get(board_pk=kwargs['pk'], tab_index=kwargs['tab_index'])
        resp = TabSerializer(target_tab)
        return Response(resp.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        target_tab = Tab.objects.get(board_pk=kwargs['pk'], tab_index=kwargs['tab_index'])
        target_tab.name = request.data["name"]
        target_tab.save()
        resp = TabSerializer(target_tab)
        return Response(resp.data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        target_tab = Tab.objects.get(board_pk=kwargs['pk'], tab_index=kwargs['tab_index'])
        target_tab.delete()
        return Response({
            "status": status.HTTP_200_OK
        }, status=status.HTTP_200_OK)

class NoteView(GenericAPIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request, *args, **kwargs):
        # print(args, kwargs)
        target_board = Board.objects.get(pk=kwargs['board_pk'])
        target_tab = Tab.objects.get(board_pk=target_board, tab_index=kwargs['tab_index'])
        target_notelist = Note.objects.filter(board_pk=kwargs['board_pk'], tab_pk=target_tab)
        resp = NoteSerializer(target_notelist, many=True).data
        return Response(resp, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        # print(args, kwargs)
        # print(request.data)
        target_board = Board.objects.get(pk=kwargs['board_pk'])
        target_tab = Tab.objects.get(board_pk=kwargs['board_pk'], tab_index=kwargs['tab_index'])
        target_type = Type.objects.get(pk=request.data['type'])

        # Pre-processing
        target_tab.max_note_index += 1
        target_tab.save()

        # Create New Note
        new_note = Note()
        new_note.user_pk = request.user
        new_note.board_pk = target_board
        new_note.tab_pk = target_tab
        new_note.type_pk = target_type
        new_note.note_index = target_tab.max_note_index
        new_note.x = request.data['x']
        new_note.y = request.data['y']
        new_note.z = request.data['z']
        new_note.width = request.data['width']
        new_note.height = request.data['height']
        new_note.content = request.data['content']
        new_note.save()

        add_history(request.user, target_board, target_tab, new_note)

        resp = NoteSerializer(new_note).data
        return Response(resp, status=status.HTTP_201_CREATED)

class NoteDetailView(GenericAPIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request, *args, **kwargs):
        # print(args, kwargs)
        # target_board = Board.objects.get(pk=kwargs['board_pk'])
        target_tab = Tab.objects.get(board_pk=kwargs['board_pk'], tab_index=kwargs['tab_index'])
        target_note = Note.objects.get(board_pk=kwargs['board_pk'], tab_pk=target_tab, note_index=kwargs['note_index'])
        resp = NoteSerializer(target_note).data
        return Response(resp, status=status.HTTP_200_OK)

    def patch(self, request, *args, **kwargs):
        # print(args, kwargs)
        # print(request.data)
        target_board = Board.objects.get(pk=kwargs['board_pk'])
        target_tab = Tab.objects.get(board_pk=kwargs['board_pk'], tab_index=kwargs['tab_index'])
        target_note = Note.objects.get(board_pk=kwargs['board_pk'], tab_pk=target_tab, note_index=kwargs['note_index'])

        for key, value in dict(request.data).items():
            setattr(target_note, key, value[0])

        target_note.save()
        add_history(request.user, target_board, target_tab, target_note)
        resp = NoteSerializer(target_note).data
        return Response(resp, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        # print(args, kwargs)
        # target_board = Board.objects.get(pk=kwargs['board_pk'])
        target_tab = Tab.objects.get(board_pk=kwargs['board_pk'], tab_index=kwargs['tab_index'])
        target_note = Note.objects.get(board_pk=kwargs['board_pk'], tab_pk=target_tab, note_index=kwargs['note_index'])
        target_note.delete()
        return Response({
            "status": status.HTTP_200_OK
        }, status=status.HTTP_200_OK)

class TypeListView(GenericAPIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request, *args, **kwargs):
        type_list = Type.objects.all()
        resp = TypeSerializer(type_list, many=True).data
        return Response(resp, status=status.HTTP_200_OK)

class TypeDetailView(GenericAPIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request, *args, **kwargs):
        target_type = Type.objects.get(pk=kwargs['type_pk'])
        resp = TypeSerializer(target_type).data
        return Response(resp, status=status.HTTP_200_OK)

class HistoryView(GenericAPIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request, *args, **kwargs):
        # print(args, kwargs)
        if kwargs.get('board_pk') == None:
            return Response({
                "status": status.HTTP_404_NOT_FOUND,
            }, status.HTTP_404_NOT_FOUND)

        history_query = Q()
        for key, value in kwargs.items():
            if key == 'board_pk':
                history_query = history_query & Q(**{'board_id': value})
            elif key == 'tab_index':
                history_query = history_query & Q(**{'tab_index': value})
            elif key == 'note_index':
                history_query = history_query & Q(**{'note_index': value})

        history_list = History.objects.filter(history_query)
        resp = HistorySerializer(history_list, many=True).data
        return Response(resp, status=status.HTTP_200_OK)
