from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

# Create your views here.
from rest_framework.generics import GenericAPIView

class BoardView(GenericAPIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request, *args, **kwargs):
        return Response("DEBUG")

    def post(self, request, *args, **kwargs):
        return Response("DEBUG")

    def put(self, request, *args, **kwargs):
        return Response("DEBUG")

    def delete(self, request, *args, **kwargs):
        return Response("DEBUG")


class TabView(GenericAPIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request, *args, **kwargs):
        return Response("DEBUG")

    def post(self, request, *args, **kwargs):
        return Response("DEBUG")

    def put(self, request, *args, **kwargs):
        return Response("DEBUG")

    def delete(self, request, *args, **kwargs):
        return Response("DEBUG")

class NoteView(GenericAPIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request, *args, **kwargs):
        return Response("DEBUG")

    def post(self, request, *args, **kwargs):
        return Response("DEBUG")

    def patch(self, request, *args, **kwargs):
        return Response("DEBUG")

    def delete(self, request, *args, **kwargs):
        return Response("DEBUG")

class TypeView(GenericAPIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request, *args, **kwargs):
        return Response("DEBUG")

    def post(self, request, *args, **kwargs):
        return Response("DEBUG")

    def delete(self, request, *args, **kwargs):
        return Response("DEBUG")

class HistoryView(GenericAPIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request, *args, **kwargs):
        return Response("DEBUG")

    def post(self, request, *args, **kwargs):
        return Response("DEBUG")

    def delete(self, request, *args, **kwargs):
        return Response("DEBUG")