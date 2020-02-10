# -*- coding: utf-8 -*-
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN
from rest_framework.views import APIView
from rest_framework.throttling import ScopedRateThrottle
from rest_framework import viewsets, mixins, filters
from .models import Problem, ProblemData, ProblemTag, ChoiceProblem
from .serializers import ProblemSerializer, ProblemDataSerializer, ProblemTagSerializer,ChoiceProblemSerializer
from .permission import ManagerOnly, AuthOnly
from django.shortcuts import render
from django.views.generic import View
from django.shortcuts import HttpResponse
from django.http import FileResponse

import base64
import zipfile
import shutil
import os


class ProblemView(viewsets.GenericViewSet, mixins.DestroyModelMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin):
    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer
    filter_fields = ('auth',)
    permission_classes = (AuthOnly,)
    throttle_scope = "post"
    throttle_classes = [ScopedRateThrottle, ]

class ChoiceProblemView(viewsets.ModelViewSet):
    queryset = ChoiceProblem.objects.all()
    serializer_class = ChoiceProblemSerializer
    filter_fields = ('ChoiceProblemId','des')
    throttle_scope = "post"

class ProblemDataView(viewsets.ModelViewSet):

    queryset = ProblemData.objects.extra(
        select={'t': 'problem+0'}).extra(order_by=["-t"])
    serializer_class = ProblemDataSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (ManagerOnly,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filter_fields = ('auth','oj',)
    search_fields = ('tag', 'title')
    throttle_scope = "post"
    throttle_classes = [ScopedRateThrottle, ]


class ProblemTagView(viewsets.ModelViewSet):
    queryset = ProblemTag.objects.all()
    serializer_class = ProblemTagSerializer
    permission_classes = (ManagerOnly,)
    throttle_scope = "post"
    throttle_classes = [ScopedRateThrottle, ]


class UploadFileAPIView(APIView):
    def post(self, request, format=None):
        type = request.session.get('type', 1)
        if type == 1:
            return Response("Admin Only", status=HTTP_403_FORBIDDEN)

        myFile = request.FILES.get("file", None)    # 获取上传的文件，如果没有文件，则默认为None
        if not myFile:
            return Response("no file", status=HTTP_400_BAD_REQUEST)

        destination = open("./ProblemData/" +
                           myFile.name, 'wb+')    # 打开特定的文件进行二进制的写操作
        for chunk in myFile.chunks():      # 分块写入文件
            destination.write(chunk)
        destination.close()

        # dirname = myFile.name.split(".")[0]
        # try:
        #     shutil.rmtree("../DataServer/problemdata/" +
        #                   dirname+"/", ignore_errors=True)
        #     f = zipfile.ZipFile("../DataServer/problemdata/"+myFile.name, 'r')
        #     for file1 in f.namelist():
        #         f.extract(file1, "../DataServer/problemdata/"+dirname+"/")
        # except:
        #     shutil.rmtree("../DataServer/problemdata/" +
        #                   dirname+"/", ignore_errors=True)
        #     os.remove("../DataServer/problemdata/"+myFile.name)
        #     return Response("extract zip fail", status=HTTP_400_BAD_REQUEST)

        return Response('upload success', HTTP_200_OK)


def filedown(request):
    name = request.GET.get('name')
    file = open('./ProblemData/'+name+'.zip','rb')
    response = FileResponse(file)
    response['Content-Type']='application/msword'
    response['Content-Disposition']='attachment;filename='+name+'.zip'
    return response

def showpic(request):
    name = request.GET.get('ProblemId')
    file = open('./ProblemData/'+name+'.jpg','rb')
    #file = open('./ProblemData/1.jpg','rb')
    result = file.read()

    result = base64.b64encode(result)
    return HttpResponse(result, content_type='image/jpg')


