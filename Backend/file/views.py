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

class FileUploadView(APIView):
    permission_classes = [AllowAny]
    parser_class = (FileUploadParser,)

    def post(self, request, *args, **kwargs):
        # 이 케이스는 이미지 파일 이외의 것을 의미한다.
        file_serializer = FileSerializer(data=request.data)
        if file_serializer.is_valid():
            model_obj = file_serializer.save()
            model_obj.filename = request.FILES['file'].name
            model_obj.hex_name = str(model_obj).split("/")[-1]
            model_obj.save()
            result = file_serializer.data

            if request.FILES['file'].name.split(".")[-1] in settings.IMAGE_TYPE:
                file_url = settings.BACKEND_URL + "api/v1/" + str(model_obj)
            else:
                file_url = settings.BACKEND_URL + "api/v1/file/download/" + "/".join(str(model_obj).split("/")[4:])

            resp = {
                'file_url': file_url,
                'original_filename': result["filename"],
            }

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
