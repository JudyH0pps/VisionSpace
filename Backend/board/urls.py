from django.urls import path
from .views import *

app_name = 'board'

urlpatterns = [
    path('', BoardView.as_view(), name="board"),
    path('<int:pk>', BoardDetailView.as_view(), name="board"),
    path('<int:pk>/join/', BoardJoinView.as_view(), name="board_join"),
    path('<int:pk>/tab/', TabView.as_view(), name="tab"),
    path('<int:pk>/tab/<int:tab_index>/', TabDetailView.as_view(), name="tab_detail"),
    path('<int:board_pk>/tab/<int:tab_index>/note/', NoteView.as_view(), name="note"),
    path('<int:board_pk>/tab/<int:tab_index>/note/<int:note_index>/', NoteDetailView.as_view(), name="note_detail"),
    path('type/', TypeListView.as_view(), name="type"),
    path('type/<int:type_pk>/', TypeDetailView.as_view(), name="type_detail"),
    path('<int:board_pk>/history/', HistoryView.as_view(), name="board_history"),
    path('<int:board_pk>/tab/<int:tab_index>/history/', HistoryView.as_view(), name="tab_history"),
    path('<int:board_pk>/tab/<int:tab_index>/note/<int:note_index>/history/', HistoryView.as_view(), name="note_history"),
    # path('history/', HistoryView.as_view(), name="history"),
]