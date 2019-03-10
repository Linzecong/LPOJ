# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from rest_framework import viewsets, mixins
from .models import Problem, ProblemData, ProblemTag
from .serializers import ProblemSerializer, ProblemDataSerializer, ProblemTagSerializer
from .permission import ManagerOnly, AuthOnly
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

class ProblemView(viewsets.GenericViewSet, mixins.DestroyModelMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin):
    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer
    filter_fields = ('auth',)
    permission_classes = (AuthOnly,)


class ProblemDataView(viewsets.ModelViewSet):
    queryset = ProblemData.objects.all()
    serializer_class = ProblemDataSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (ManagerOnly,)
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('auth',)


class ProblemTagView(viewsets.ModelViewSet):
    queryset = ProblemTag.objects.all()
    serializer_class = ProblemTagSerializer
    permission_classes = (ManagerOnly,)

class UploadFileAPIView(APIView):
    def post(self, request, format=None):
        myFile =request.FILES.get("file", None)    # 获取上传的文件，如果没有文件，则默认为None 
        if not myFile: 
            return Response("no file", status=HTTP_400_BAD_REQUEST)
        destination = open("../Dataserver/problemdata/"+myFile.name,'wb+')    # 打开特定的文件进行二进制的写操作 
        for chunk in myFile.chunks():      # 分块写入文件 
            destination.write(chunk) 
        destination.close() 
        return Response('upload success', HTTP_200_OK)