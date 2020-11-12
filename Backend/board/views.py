from django.shortcuts import render
from django.http import HttpResponse, Http404
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Board, Tab, Type, Note, History, User_Board
from .serializers import BoardSerializer, BoardViewSerializer, TabSerializer, TypeSerializer, NoteSerializer, HistoryViewSerializer, TabViewSerializer, NoteViewSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework import mixins
from rest_framework.generics import GenericAPIView
from rest_framework import status
from django.db.models import Q
from django.http import HttpRequest, QueryDict
from file.views import FileUploadView

class CustomPagination(PageNumberPagination):
    page_size = 20
    page_query_param = 'page'

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
    new_history.type_index = note.type_pk.pk
    new_history.content = note.content
    new_history.color = note.color
    new_history.save()
    return

class BoardView(mixins.CreateModelMixin, 
                    mixins.ListModelMixin,
                    GenericAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    lookup_field = 'session_id'
    pagination_class = CustomPagination

    def get_queryset(self):
        if self.request.user:
            queryset = Board.objects.filter(user_list=self.request.user).order_by('-pk')
        else:
            queryset = Board.objects.none()
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = BoardViewSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = BoardViewSerializer(queryset, many=True)
        return Response(serializer.data)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        create_request = self.create(request, *args, **kwargs)
        created_board = Board.objects.get(pk=create_request.data['id'])
        created_board.super_admin = request.user
        created_board.save()

        new_member = User_Board()
        new_member.board_pk = created_board
        new_member.user_pk = request.user
        new_member.is_admin = True
        new_member.save()

        new_tab = Tab()       
        new_tab.board_pk = created_board
        new_tab.tab_index = created_board.max_tab_index
        new_tab.name = "tab1"
        new_tab.save()

        created_board.max_tab_index += 1
        created_board.save()

        resp = BoardViewSerializer(created_board).data
        return Response(resp, status=status.HTTP_201_CREATED)

class BoardDetailView(mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.DestroyModelMixin,
                        GenericAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    lookup_field = 'session_id'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = BoardViewSerializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        if request.user != instance.super_admin:
            return Response({
                "status": status.HTTP_401_UNAUTHORIZED
            }, status=status.HTTP_401_UNAUTHORIZED)

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        resp = BoardViewSerializer(instance)
        return Response(resp.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user != instance.super_admin:
            return Response({
                "status": status.HTTP_401_UNAUTHORIZED
            }, status=status.HTTP_401_UNAUTHORIZED)

        self.perform_destroy(instance)
        return Response({
            "status": status.HTTP_204_NO_CONTENT
        }, status=status.HTTP_204_NO_CONTENT)

    def get(self, request, *args, **kwargs):
        if not request.user:
            return Response({
                "status": status.HTTP_401_UNAUTHORIZED
            }, status=status.HTTP_401_UNAUTHORIZED)
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
                "status": status.HTTP_200_OK
            }, status=status.HTTP_200_OK)

        new_member = User_Board()
        new_member.board_pk = target_board
        new_member.user_pk = request.user
        new_member.is_admin = False
        new_member.save()
        return Response({
            "status": status.HTTP_200_OK
        }, status=status.HTTP_200_OK)

class BoardDisconnectView(GenericAPIView):
    permission_classes = (IsAuthenticated, )
    def post(self, request, *args, **kwargs):
        try:
            target_board = Board.objects.get(session_id=kwargs['session_id'])
        except:
            return Response({
                "status": status.HTTP_204_NO_CONTENT
            }, status=status.HTTP_204_NO_CONTENT)

        user_search = User_Board.objects.filter(board_pk_id=target_board, user_pk_id=request.user)
        if not user_search:
            return Response({
                "status": status.HTTP_200_OK
            }, status=status.HTTP_200_OK)
        
        user_search.delete()

        if target_board.super_admin == request.user:
            # 여기에서 한 가지 문제점: 보드가 통으로 폭파되는데 기존에 채팅 세션에 있던 사람은 그럼 폭파를 어떻게...
            target_board.delete()

        return Response({
            "status": status.HTTP_200_OK
        }, status=status.HTTP_200_OK)

class TabView(GenericAPIView):
    serializer_class = TabSerializer
    permission_classes = (IsAuthenticated, )
    def get(self, request, *args, **kwargs):
        target_board = Board.objects.get(session_id=kwargs['session_id'])
        tab_list = Tab.objects.filter(board_pk_id=target_board)
        resp = TabViewSerializer(tab_list, many=True)
        return Response(resp.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        target_board = Board.objects.get(session_id=kwargs['session_id'])
        board_user_search = User_Board.objects.filter(board_pk=target_board, user_pk=request.user)
        if len(board_user_search) == 0:
            return Response({
                "status": status.HTTP_401_UNAUTHORIZED
            }, status=status.HTTP_401_UNAUTHORIZED)

        new_tab = Tab()       
        new_tab.board_pk = target_board
        new_tab.tab_index = target_board.max_tab_index
        new_tab.name = request.data["name"]
        new_tab.save()

        target_board.max_tab_index += 1
        target_board.save()

        resp = TabViewSerializer(new_tab)
        return Response(
            resp.data, status=status.HTTP_201_CREATED
        )

class TabDetailView(GenericAPIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request, *args, **kwargs):
        target_board = Board.objects.get(session_id=kwargs['session_id'])
        target_tab = Tab.objects.get(board_pk=target_board, tab_index=kwargs['tab_index'])
        resp = TabViewSerializer(target_tab)
        return Response(resp.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        target_board = Board.objects.get(session_id=kwargs['session_id'])
        board_user_search = User_Board.objects.filter(board_pk=target_board, user_pk=request.user)
        if len(board_user_search) == 0:
            return Response({
                "status": status.HTTP_401_UNAUTHORIZED
            }, status=status.HTTP_401_UNAUTHORIZED)

        target_tab = Tab.objects.get(board_pk=target_board, tab_index=kwargs['tab_index'])
        target_tab.name = request.data["name"]
        target_tab.save()
        resp = TabViewSerializer(target_tab)
        return Response(resp.data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        target_board = Board.objects.get(session_id=kwargs['session_id'])
        board_user_search = User_Board.objects.filter(board_pk=target_board, user_pk=request.user)
        if len(board_user_search) == 0:
            return Response({
                "status": status.HTTP_401_UNAUTHORIZED
            }, status=status.HTTP_401_UNAUTHORIZED)

        target_tab = Tab.objects.get(board_pk=target_board, tab_index=kwargs['tab_index'])
        target_tab.delete()
        return Response({
            "status": status.HTTP_200_OK
        }, status=status.HTTP_200_OK)

class BoardNoteView(GenericAPIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request, *args, **kwargs):
        target_board = Board.objects.get(session_id=kwargs['session_id'])
        target_notelist = Note.objects.filter(board_pk=target_board)
        resp = NoteViewSerializer(target_notelist, many=True).data
        return Response(resp, status=status.HTTP_200_OK)

class NoteView(GenericAPIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request, *args, **kwargs):
        target_board = Board.objects.get(session_id=kwargs['session_id'])
        target_tab = Tab.objects.get(board_pk=target_board, tab_index=kwargs['tab_index'])
        target_notelist = Note.objects.filter(board_pk=target_board, tab_pk=target_tab)
        resp = NoteViewSerializer(target_notelist, many=True).data
        return Response(resp, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        target_board = Board.objects.get(session_id=kwargs['session_id'])
        board_user_search = User_Board.objects.filter(board_pk=target_board, user_pk=request.user)
        if len(board_user_search) == 0:
            return Response({
                "status": status.HTTP_401_UNAUTHORIZED
            }, status=status.HTTP_401_UNAUTHORIZED)

        target_tab = Tab.objects.get(board_pk=target_board, tab_index=kwargs['tab_index'])
        target_type = Type.objects.get(pk=request.data['type'])

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
        new_note.color = request.data['color']
        
        if target_type.pk == 1:
            # 만약에 type이 1이면 그냥 그대로 내보내면 된다.
            new_note.content = request.data['content']
        
        elif target_type.pk == 2:
            # 만약에 type이 2이면 파일이라는 뜻이다. 이 부분은 file app의 파일 업로드 기능을 활용하면 될 것으로 보인다.
            new_request = HttpRequest()
            body_data = QueryDict('', mutable=True)
            body_data.update({
                'file': request.FILES["content"]
            })
            new_request.method = 'POST'
            new_request.META = request.META
            new_request.META["PATH_INFO"] = '/api/v1/file/'
            new_request.FILES["file"] = request.FILES["content"] # 새로운 리퀘스트를 만들 때 new_request.FILES에도 파일을 넣어야 하는 점을 잊지 말자!
            new_request.data = body_data
            uploaded_file = FileUploadView.as_view()(new_request, *args, **kwargs)
            new_note.content = "{} [{}]".format(uploaded_file.data["file_url"], uploaded_file.data["original_filename"])

        new_note.save()

        # Pre-processing
        target_tab.max_note_index += 1
        target_tab.save()

        add_history(request.user, target_board, target_tab, new_note)

        resp = NoteViewSerializer(new_note).data
        return Response(resp, status=status.HTTP_201_CREATED)

class NoteDetailView(GenericAPIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request, *args, **kwargs):
        target_board = Board.objects.get(session_id=kwargs['session_id'])
        target_tab = Tab.objects.get(board_pk=target_board, tab_index=kwargs['tab_index'])
        target_note = Note.objects.get(board_pk=target_board, tab_pk=target_tab, note_index=kwargs['note_index'])
        resp = NoteViewSerializer(target_note).data
        return Response(resp, status=status.HTTP_200_OK)

    def patch(self, request, *args, **kwargs):
        target_board = Board.objects.get(session_id=kwargs['session_id'])
        board_user_search = User_Board.objects.filter(board_pk=target_board, user_pk=request.user)
        if len(board_user_search) == 0:
            return Response({
                "status": status.HTTP_401_UNAUTHORIZED
            }, status=status.HTTP_401_UNAUTHORIZED)

        target_tab = Tab.objects.get(board_pk=target_board, tab_index=kwargs['tab_index'])
        target_note = Note.objects.get(board_pk=target_board, tab_pk=target_tab, note_index=kwargs['note_index'])
        
        # if target_note.user_pk != request.user:
        #     return Response({
        #         "status": status.HTTP_401_UNAUTHORIZED
        #     }, status=status.HTTP_401_UNAUTHORIZED)

        request_info = dict(request.data)
        for key, value in request_info.items():
            setattr(target_note, key, value[0])
        
        # target_note.user_pk = request.user
        target_note.save()

        # Changing Coordinates cannot be co-operated with changing content
        if "x" not in request_info.keys() and "y" not in request_info.keys() and "z" not in request_info.keys():
            add_history(request.user, target_board, target_tab, target_note)

        resp = NoteViewSerializer(target_note).data
        return Response(resp, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        target_board = Board.objects.get(session_id=kwargs['session_id'])
        target_tab = Tab.objects.get(board_pk=target_board, tab_index=kwargs['tab_index'])
        target_note = Note.objects.get(board_pk=target_board, tab_pk=target_tab, note_index=kwargs['note_index'])
        if target_note.user_pk != request.user:
            return Response({
                "status": status.HTTP_401_UNAUTHORIZED
            }, status=status.HTTP_401_UNAUTHORIZED)

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
        if kwargs.get('session_id') == None:
            return Response({
                "status": status.HTTP_404_NOT_FOUND,
            }, status.HTTP_404_NOT_FOUND)

        history_query = Q()
        for key, value in kwargs.items():
            if key == 'session_id':
                target_board = Board.objects.get(session_id=kwargs['session_id'])
                history_query = history_query & Q(**{'board_id': target_board.pk})
            elif key == 'tab_index':
                history_query = history_query & Q(**{'tab_index': value})
            elif key == 'note_index':
                history_query = history_query & Q(**{'note_index': value})

        history_list = History.objects.filter(history_query)
        resp = HistoryViewSerializer(history_list, many=True).data
        return Response(resp, status=status.HTTP_200_OK)

class TimeMachineView(GenericAPIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request, *args, **kwargs):
        pass

    def post(self, request, *args, **kwargs):
        pass

class TimeMachineDetailView(GenericAPIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request, *args, **kwargs):
        pass

    def post(self, request, *args, **kwargs):
        pass

    def delete(self, request, *args, **kwargs):
        pass