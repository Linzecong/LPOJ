# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination
from .permission import ManagerOnly,LoginOnly,UserOnly,UserOnly2
from .models import ContestAnnouncement,ContestRank,ContestRatingChange, ContestBoard, ContestComment, ContestInfo, ContestProblem, ContestRegister
from .serializers import ContestRankSerializer,ContestRatingChangeSerializer, ContestAnnouncementSerializer,ContestBoardSerializer,ContestCommentSerializer,ContestInfoSerializer,ContestProblemSerializer, ContestRegisterSerializer
from django_filters.rest_framework import DjangoFilterBackend
import datetime
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework.throttling import ScopedRateThrottle


class ContestAnnouncementView(viewsets.ModelViewSet):
    queryset = ContestAnnouncement.objects.all()
    serializer_class = ContestAnnouncementSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (ManagerOnly,)
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ("contestid",)
    throttle_scope  = "post"
    throttle_classes =[ScopedRateThrottle,]

class ContestBoardView(viewsets.ModelViewSet):
    queryset = ContestBoard.objects.all()
    serializer_class = ContestBoardSerializer
    # pagination_class = LimitOffsetPagination
    permission_classes = (UserOnly,)
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ("contestid",)
    throttle_scope  = "post"
    throttle_classes =[ScopedRateThrottle,]

class ContestRankView(viewsets.ModelViewSet):
    queryset = ContestRank.objects.all()
    serializer_class = ContestRankSerializer
    permission_classes = (UserOnly,)
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ("contestid","username")
    throttle_scope  = "post"
    throttle_classes =[ScopedRateThrottle,]


class ContestCommentView(viewsets.ModelViewSet):
    queryset = ContestComment.objects.all()
    serializer_class = ContestCommentSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (UserOnly2,)
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ("contestid",)
    throttle_scope  = "post"
    throttle_classes =[ScopedRateThrottle,]

class ContestInfoView(viewsets.ModelViewSet):
    queryset = ContestInfo.objects.all()
    serializer_class = ContestInfoSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (ManagerOnly,)
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ("begintime","level")
    throttle_scope  = "post"
    throttle_classes =[ScopedRateThrottle,]

class ContestComingInfoView(viewsets.ModelViewSet):
    queryset = ContestInfo.objects.filter(begintime__gte=datetime.datetime.now())
    serializer_class = ContestInfoSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (ManagerOnly,)
    throttle_scope  = "post"
    throttle_classes =[ScopedRateThrottle,]

class ContestProblemView(viewsets.ModelViewSet):
    queryset = ContestProblem.objects.all().order_by('rank')
    serializer_class = ContestProblemSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (ManagerOnly,)
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('contestid',)
    throttle_scope  = "post"
    throttle_classes =[ScopedRateThrottle,]

class ContestRegisterView(viewsets.ModelViewSet):
    queryset = ContestRegister.objects.all()
    serializer_class = ContestRegisterSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend,)
    permission_classes = (UserOnly2,)
    filter_fields = ('user', "contestid")
    throttle_scope  = "post"
    throttle_classes =[ScopedRateThrottle,]

class ContestRatingChangeView(viewsets.ModelViewSet):
    queryset = ContestRatingChange.objects.all()
    serializer_class = ContestRatingChangeSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (ManagerOnly,)
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('user', "contestid")
    throttle_scope  = "post"
    throttle_classes =[ScopedRateThrottle,]

class CurrentTimeView(APIView):
    def get(self,request):
        return Response(datetime.datetime.now(), HTTP_200_OK)