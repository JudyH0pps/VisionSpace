from django.shortcuts import get_object_or_404
from django.http import HttpResponse, Http404
from rest_framework.permissions import (AllowAny, IsAuthenticated, BasePermission)
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import FileSerializer
from django.conf import settings
import os, urllib, mimetypes
from .models import File
# Create your views here.

class FileUploadView(APIView):
    permission_classes = [AllowAny]
    parser_class = (FileUploadParser,)

    def post(self, request, *args, **kwargs):
        file_serializer = FileSerializer(data=request.data)
        if file_serializer.is_valid():
            # if request.FILES:
            #     if 'file' in request.FILES.keys():
            #         file_serializer.filename = request.FILES['file'].name
            model_obj = file_serializer.save()
            model_obj.filename = request.FILES['file'].name
            model_obj.hex_name = str(model_obj).split("/")[-1]
            model_obj.save()
            resp = file_serializer.data
            return Response(resp, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FileDownloadView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        target_file = get_object_or_404(File, hex_name=kwargs["file_id"])
        url = target_file.file.url[1:]
        file_url = urllib.parse.unquote(url)
        if os.path.exists(file_url):
            with open(file_url, 'rb') as fh:
                quote_file_url = urllib.parse.quote(target_file.filename.encode('utf-8'))
                response = HttpResponse(fh.read(), content_type=mimetypes.guess_type(file_url)[0])
                response['Content-Disposition'] = 'attachment;filename*=UTF-8\'\'%s' % quote_file_url
                return response
            raise Http404
