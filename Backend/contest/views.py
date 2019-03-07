# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination
from .permission import ManagerOnly
from .models import ContestAnnouncement,ContestRank, ContestBoard, ContestComment, ContestInfo, ContestProblem, ContestRegister
from .serializers import ContestRankSerializer, ContestAnnouncementSerializer,ContestBoardSerializer,ContestCommentSerializer,ContestInfoSerializer,ContestProblemSerializer, ContestRegisterSerializer
from django_filters.rest_framework import DjangoFilterBackend

class ContestAnnouncementView(viewsets.ModelViewSet):
    queryset = ContestAnnouncement.objects.all()
    serializer_class = ContestAnnouncementSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (ManagerOnly,)
    # filter_backends = (DjangoFilterBackend,)
    # filter_fields = ('user', 'result', "contest")

class ContestBoardView(viewsets.ModelViewSet):
    queryset = ContestBoard.objects.all()
    serializer_class = ContestBoardSerializer
    # pagination_class = LimitOffsetPagination
    # permission_classes = (ManagerOnly,)# 将来要改写成重写post形式
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ("contestid",)

class ContestRankView(viewsets.ModelViewSet):
    queryset = ContestRank.objects.all()
    serializer_class = ContestRankSerializer
     # permission_classes = (ManagerOnly,)# 将来要改写成重写post形式
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ("contestid","username")


class ContestCommentView(viewsets.ModelViewSet):
    queryset = ContestComment.objects.all()
    serializer_class = ContestCommentSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (ManagerOnly,)
    # filter_backends = (DjangoFilterBackend,)
    # filter_fields = ('user', 'result', "contest")

class ContestInfoView(viewsets.ModelViewSet):
    queryset = ContestInfo.objects.all()
    serializer_class = ContestInfoSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (ManagerOnly,)
    # filter_backends = (DjangoFilterBackend,)
    # filter_fields = ('user', 'result', "contest")

class ContestProblemView(viewsets.ModelViewSet):
    queryset = ContestProblem.objects.all().order_by('rank')
    serializer_class = ContestProblemSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (ManagerOnly,)
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('contestid',)

class ContestRegisterView(viewsets.ModelViewSet):
    queryset = ContestRegister.objects.all()
    serializer_class = ContestRegisterSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('user', "contestid")
