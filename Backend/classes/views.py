# -*- coding: utf-8 -*-
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets,filters
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST,HTTP_204_NO_CONTENT
from rest_framework.views import APIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.throttling import ScopedRateThrottle
from .models import Classes
from .models import ClassStudentData
from .serializers import ClassDataSerializer
from .serializers import ClassStudentDataSerializer
# Create your views here.


class ClassDataView(viewsets.ModelViewSet):
    queryset = Classes.objects.all()
    serializer_class = ClassDataSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filter_fields = ('className',)
    search_fields = ('className', 'classSize')
    pagination_class = LimitOffsetPagination
    throttle_scope = "post"

class ClassDataAPIView(APIView):
    queryset = Classes.objects.all()
    serializer_class = ClassDataSerializer
    def post(self, request, format = None):
        data = request.data.copy()
        serializer = ClassDataSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response('AddOk', status=HTTP_200_OK)
        return Response("AddFail", status=HTTP_400_BAD_REQUEST)

class DeleteClassDataAPIView(APIView):
    queryset = Classes.objects.all()
    serializer_class = ClassDataSerializer
    def delete(self, request, format=None):
        data = request.data.copy()
        CName = data["className"]
        if Classes.objects.filter(className__exact=CName):
            if Classes.objects.filter(className__exact=CName).delete():
                return Response("DeleteOk", status=HTTP_200_OK)
        else:
            return Response("AlreadyDelete", HTTP_200_OK)

        return Response("DeleteFail", status=HTTP_400_BAD_REQUEST)


class ClassStudentDataView(viewsets.ModelViewSet):
    queryset = ClassStudentData.objects.all()
    serializer_class = ClassStudentDataSerializer
    filter_fields = ('studentUserName','studentNumber','className','studentRealName')
    search_fields = ('studentUserName','studentNumber','className','studentRealName')
    throttle_scope = "post"
    pagination_class = LimitOffsetPagination

class ClassStudentDataAPIView(APIView):
    queryset = ClassStudentData.objects.all()
    serializer_class = ClassStudentDataSerializer
    def post(self, request, format=None):
        data = request.data.copy()
        Name = data["studentUserName"]
        RName = data["studentRealName"]
        CName = data["className"]
        Number = data["studentNumber"]
        serializer = ClassStudentDataSerializer(data=data)

        if serializer.is_valid(raise_exception=True):
            if ClassStudentData.objects.filter(studentUserName__exact=Name,className__exact=CName,studentNumber__exact=Number):
                print("case1")
                return Response("RepeatJoin", HTTP_200_OK)

            print("case2")
            serializer.save()
            return Response("JoinOk", status=HTTP_200_OK)

        return Response("JoinFail", status=HTTP_400_BAD_REQUEST)

class QuitClassAPIView(APIView):
    queryset = ClassStudentData.objects.all()
    serializer_class = ClassStudentDataSerializer
    def delete(self, request, format=None):
        data = request.data.copy()
        Name = data["studentUserName"]
        RName = data["studentRealName"]
        CName = data["className"]
        Number = data["studentNumber"]
        # if ClassStudentData.objects.filter(studentUserName__exact=Name,className__exact=CName,studentNumber__exact=Number):
        if ClassStudentData.objects.filter(studentUserName__exact=Name,className__exact=CName,studentNumber__exact=Number).delete():
                return Response("QuitOk", status=HTTP_200_OK)
        else:
            return Response("AlreadyQuit", HTTP_200_OK)

        return Response("QuitFail", status=HTTP_400_BAD_REQUEST)


