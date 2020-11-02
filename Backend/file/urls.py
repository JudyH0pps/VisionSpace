from django.urls import path
from .views import *

urlpatterns = [
    path('', FileUploadView.as_view()),
    path('download/<str:file_id>', FileDownloadView.as_view()),
]
