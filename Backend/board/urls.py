from django.urls import path
from .views import *

app_name = 'board'

urlpatterns = [
    path('', BoardView.as_view(), name="board"),
    path('<str:session_id>/', BoardDetailView.as_view(), name="board"),
    path('<str:session_id>/join/', BoardJoinView.as_view(), name="board_join"),
    path('<str:session_id>/note/', BoardNoteView.as_view(), name="board_note"),
    path('<str:session_id>/tab/', TabView.as_view(), name="tab"),
    path('<str:session_id>/tab/<int:tab_index>/', TabDetailView.as_view(), name="tab_detail"),
    path('<str:session_id>/tab/<int:tab_index>/note/', NoteView.as_view(), name="note"),
    path('<str:session_id>/tab/<int:tab_index>/note/<int:note_index>/', NoteDetailView.as_view(), name="note_detail"),
    path('type/', TypeListView.as_view(), name="type"),
    path('type/<int:type_pk>/', TypeDetailView.as_view(), name="type_detail"),
    path('<str:session_id>/history/', HistoryView.as_view(), name="board_history"),
    path('<str:session_id>/tab/<int:tab_index>/history/', HistoryView.as_view(), name="tab_history"),
    path('<str:session_id>/tab/<int:tab_index>/note/<int:note_index>/history/', HistoryView.as_view(), name="note_history"),
]