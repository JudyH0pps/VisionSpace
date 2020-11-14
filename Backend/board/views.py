from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, Http404
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Board, Tab, Type, Note, History, User_Board, Time_Machine, Capsule
from .serializers import BoardSerializer, BoardViewSerializer, TabSerializer, TypeSerializer, NoteSerializer, HistoryViewSerializer, TabViewSerializer, NoteViewSerializer, TimeMachineViewSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework import mixins
from rest_framework.generics import GenericAPIView
from rest_framework import status
from django.db.models import Q
from django.http import HttpRequest, QueryDict
from django.contrib.auth import get_user_model
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
        if len(board_user_search) == 0 or target_board.super_admin != request.user:
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
        
        if target_type.pk == 1 or target_type.pk == 3:
            # 만약에 type이 1이나 3이면 그냥 그대로 내보내면 된다.
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

        # After 11-14, history will be added only when delete note
        # add_history(request.user, target_board, target_tab, new_note)

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
        add_history(request.user, target_board, target_tab, target_note)    # Now history will be stacked only when delete notes

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

class HistoryView(mixins.ListModelMixin, GenericAPIView):
    permission_classes = (IsAuthenticated, )
    pagination_class = CustomPagination

    def get_queryset(self, **kwargs):
        history_query = Q()
        for key, value in kwargs.items():
            if key == 'session_id':
                target_board = Board.objects.get(session_id=kwargs['session_id'])
                history_query = history_query & Q(**{'board_id': target_board.pk})
            elif key == 'tab_index':
                history_query = history_query & Q(**{'tab_index': value})
            elif key == 'note_index':
                history_query = history_query & Q(**{'note_index': value})
        
        history_query = history_query & Q(**{'user_pk': self.request.user})
        history_query = history_query & Q(**{'activate': True})
        result = History.objects.filter(history_query).order_by("-pk")
        return result

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset(**kwargs))
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = HistoryViewSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        # history_list = History.objects.filter(queryset)
        resp = HistoryViewSerializer(queryset, many=True).data
        return Response(resp, status=status.HTTP_200_OK)

    def get(self, request, *args, **kwargs):
        if kwargs.get('session_id') == None:
            return Response({
                "status": status.HTTP_404_NOT_FOUND,
            }, status.HTTP_404_NOT_FOUND)

        return self.list(request, *args, **kwargs)

class HistoryDetailView(GenericAPIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request, *args, **kwargs):
        if kwargs.get('session_id') == None:
            return Response({
                "status": status.HTTP_404_NOT_FOUND,
            }, status.HTTP_404_NOT_FOUND)
        
        target_board = get_object_or_404(Board, session_id=kwargs['session_id'])
        target_history = get_object_or_404(History, board_id=target_board.pk, tab_index=kwargs['tab_index'], note_index=kwargs['note_index'])

        if target_history.user_pk != request.user:
            return Response({
                "status": status.HTTP_401_UNAUTHORIZED,
            }, status.HTTP_401_UNAUTHORIZED)

        resp = HistoryViewSerializer(target_history).data
        return Response(resp, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        # 노트를 복구해주는 로직이라고 할 수 있다. 하지만 노트를 복구하는 로직은 새로 노트를 생성할 때와는 조금 다르게 접근한다.
        target_board = get_object_or_404(Board, session_id=kwargs['session_id'])
        target_tab = get_object_or_404(Tab, board_pk=target_board, tab_index=kwargs['tab_index'])
        target_history = get_object_or_404(History, board_id=target_board.pk, tab_index=kwargs['tab_index'], note_index=kwargs['note_index'])
        target_type = get_object_or_404(Type, pk=target_history.type_index)

        # 자기 자신의 History가 아닌 것을 복구하려는 경우나, activate가 활성화 되지 않은 경우 거절하는 로직을 추가했다.
        if target_history.user_pk != request.user or target_history.activate == False:
            return Response({
                "status": status.HTTP_401_UNAUTHORIZED,
            }, status.HTTP_401_UNAUTHORIZED)

        new_note = Note()
        new_note.user_pk = request.user
        new_note.board_pk = target_board
        new_note.tab_pk = target_tab
        new_note.type_pk = target_type
        new_note.note_index = target_tab.max_note_index
        new_note.x = target_history.x
        new_note.y = target_history.y
        new_note.z = target_history.z
        new_note.width = target_history.width
        new_note.height = target_history.height
        new_note.content = target_history.content
        new_note.color = target_history.color
        new_note.save()

        # Post-processing
        target_tab.max_note_index += 1
        target_tab.save()
        target_history.activate = False
        target_history.save()

        resp = NoteViewSerializer(new_note).data
        return Response(resp, status=status.HTTP_201_CREATED)


class CustomTimeMachinePagination(PageNumberPagination):
    page_size = 10
    page_query_param = 'page'

class TimeMachineView(mixins.ListModelMixin, GenericAPIView):
    permission_classes = (IsAuthenticated, )
    pagination_class = CustomTimeMachinePagination

    def get_queryset(self, **kwargs):
        tm_query = Q()
        target_board = None

        for key, value in kwargs.items():
            if key == 'session_id':
                target_board = Board.objects.get(session_id=kwargs['session_id'])
                tm_query = tm_query & Q(**{'board_pk': target_board})
            elif key == 'tab_index':
                tm_query = tm_query & Q(**{'tab_index': value})

        result = Time_Machine.objects.filter(tm_query).order_by("-pk")
        return result

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset(**kwargs))
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = TimeMachineViewSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        resp = TimeMachineViewSerializer(queryset, many=True).data
        return Response(resp, status=status.HTTP_200_OK)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs) 

    def post(self, request, *args, **kwargs):
        # 1. 해당 보드 및 탭에 있는 노트를 가져온다.
        target_board = get_object_or_404(Board, session_id=kwargs['session_id'])
        target_tab = get_object_or_404(Tab, board_pk=target_board, tab_index=kwargs['tab_index'])
        target_notelist = Note.objects.filter(board_pk=target_board, tab_pk=target_tab)

        if target_board and target_board.super_admin != request.user:
            return Response({
                "status": status.HTTP_401_UNAUTHORIZED
            }, status=status.HTTP_401_UNAUTHORIZED)

        # 2. 타임머신 객체를 생성하고, board_pk와 tab_index를 매핑하고 저장한다. 이때 created_at은 자동으로 입력된다.
        new_time_machine = Time_Machine()
        new_time_machine.board_pk = target_board
        new_time_machine.tab_index = int(kwargs['tab_index'])
        new_time_machine.tm_index = target_tab.max_tm_index
        new_time_machine.save()

        target_tab.max_tm_index += 1
        target_tab.save()

        for note in target_notelist:
            # 3-1. 각 노트 마다 Capsule을 생성한 뒤...
            new_capsule = Capsule()
            new_capsule.user_pk = note.user_pk
            new_capsule.x = note.x
            new_capsule.y = note.y
            new_capsule.z = note.z
            new_capsule.width = note.width
            new_capsule.height = note.height
            new_capsule.type_index = note.type_pk.pk
            new_capsule.content = note.content
            new_capsule.color = note.color
            new_capsule.save()

            # 3-2. Capsule의 내용을 입력하고 저장한다.
            new_time_machine.capsule_list.add(new_capsule)

        # 4. 그 후 타임머신 시리얼라이저를 사용하고 리턴한다.
        resp = TimeMachineViewSerializer(new_time_machine).data
        
        return Response(resp, status=status.HTTP_200_OK)

class TimeMachineDetailView(GenericAPIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request, *args, **kwargs):
        target_board = get_object_or_404(Board, session_id=kwargs['session_id'])
        target_time_machine = get_object_or_404(Time_Machine, board_pk=target_board, tab_index=kwargs['tab_index'], tm_index=kwargs['tm_index'])
        # target_tab = get_object_or_404(Tab, board_pk=target_board, tab_index=kwargs['tab_index'])

        resp = TimeMachineViewSerializer(target_time_machine).data
        return Response(resp, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        target_board = get_object_or_404(Board, session_id=kwargs['session_id'])
        target_tab = get_object_or_404(Tab, board_pk=target_board, tab_index=kwargs['tab_index'])
        target_time_machine = get_object_or_404(Time_Machine, board_pk=target_board, tab_index=kwargs['tab_index'], tm_index=kwargs['tm_index'])

        if target_board and target_board.super_admin != request.user:
            return Response({
                "status": status.HTTP_401_UNAUTHORIZED
            }, status=status.HTTP_401_UNAUTHORIZED)

        current_note_list = Note.objects.filter(board_pk=target_board, tab_pk=target_tab)
        
        for note in current_note_list:
            note.delete()

        tm_info = TimeMachineViewSerializer(target_time_machine).data
        for capsule in tm_info.get('capsule_list'):
            capsule_info = dict(capsule)
            # print(capsule_info)
            new_note = Note()
            new_note.user_pk = get_object_or_404(get_user_model(), username=capsule_info["username"])   
            new_note.board_pk = target_board
            new_note.tab_pk = target_tab
            new_note.type_pk = get_object_or_404(Type, pk=capsule_info["type_index"])   
            new_note.note_index = target_tab.max_note_index
            new_note.x = capsule_info['x']
            new_note.y = capsule_info['y']
            new_note.z = capsule_info['z']
            new_note.width = capsule_info['width']
            new_note.height = capsule_info['height']
            new_note.content = capsule_info['content']
            new_note.color = capsule_info['color']
            new_note.save()

            target_tab.max_note_index += 1
            target_tab.save()
        
        resp = NoteViewSerializer(current_note_list, many=True).data
        return Response(resp, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        target_board = get_object_or_404(Board, session_id=kwargs['session_id'])
        target_time_machine = get_object_or_404(Time_Machine, board_pk=target_board, tab_index=kwargs['tab_index'], tm_index=kwargs['tm_index'])

        if target_board and target_board.super_admin != request.user:
            return Response({
                "status": status.HTTP_401_UNAUTHORIZED
            }, status=status.HTTP_401_UNAUTHORIZED)

        target_time_machine.delete()
        return Response({
            "status": status.HTTP_200_OK
        }, status=status.HTTP_200_OK)
