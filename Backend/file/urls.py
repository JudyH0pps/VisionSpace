from django.urls import path
from .views import FileUploadView, FileDownloadView

app_name = 'file'

urlpatterns = [
    path('', FileUploadView.as_view()),
    path('download/<str:file_id>', FileDownloadView.as_view()),
]
