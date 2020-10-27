from django.urls import path
from .views import *

app_name = 'board'

urlpatterns = [
    path('', BoardView.as_view(), name="board"),
    path('<int:pk>',BoardDetailView.as_view(), name="board"),
    path('tab/', TabView.as_view(), name="tab"),
    path('note/', NoteView.as_view(), name="note"),
    path('type/', TypeView.as_view(), name="type"),
    path('history/', HistoryView.as_view(), name="history"),
]