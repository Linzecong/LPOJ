# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from .models import User, UserData
from .serializers import UserSerializer, UserDataSerializer
from .permission import LoginOnly, UserOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import LimitOffsetPagination

class UserDataView(viewsets.ModelViewSet):
    queryset = UserData.objects.all().order_by('-score')
    serializer_class = UserDataSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('username',)
    permission_classes = (UserOnly,)
    pagination_class = LimitOffsetPagination


class UserView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('username',)
    permission_classes = (UserOnly,)
    pagination_class = LimitOffsetPagination

class UserLoginAPIView(APIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)
    def post(self, request, format=None):
        data = request.data
        username = data.get('username')
        password = data.get('password')
        user = User.objects.get(username__exact=username)
        if user.password == password:
            serializer = UserSerializer(user)
            new_data = serializer.data
            request.session['user_id'] = user.username
            request.session['type'] = user.type
            return Response(new_data, status=HTTP_200_OK)
        return Response('passworderror', HTTP_200_OK)

class UserLogoutAPIView(APIView):
    def get(self,request):
        if request.session.get('user_id',None) is not None:
            del request.session['user_id']
            del request.session['type']
        return Response('ok', HTTP_200_OK)


class UserRegisterAPIView(APIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        data = request.data
        username = data.get('username')
        if User.objects.filter(username__exact=username):
            return Response("usererror",HTTP_200_OK)
        serializer = UserSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data,status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)




