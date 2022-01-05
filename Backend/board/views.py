from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.pagination import LimitOffsetPagination
from .serializers import BoardSerializer,SettingBoardSerializer, DailyBoardSerializer, TeamBoardSerializer, DailyContestBoardSerializer
from .permission import ManagerOnly
from .models import Board, DailyBoard, TeamBoard, DailyContestBoard,SettingBoard
import datetime

class SettingBoardView(viewsets.ModelViewSet):
    queryset = SettingBoard.objects.all()
    serializer_class = SettingBoardSerializer
    permission_classes = (ManagerOnly,)
    throttle_scope = "post"
    throttle_classes = [ScopedRateThrottle, ]


class BoardView(viewsets.ModelViewSet):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    filter_fields = ('username',)
    pagination_class = LimitOffsetPagination
    permission_classes = (ManagerOnly,)
    throttle_scope = "post"
    throttle_classes = [ScopedRateThrottle, ]



class DailyBoardView(viewsets.ModelViewSet):
    queryset = DailyBoard.objects.filter(collecttime__gte=datetime.datetime.now(
    )-datetime.timedelta(days=10)).order_by('collecttime') # 这里有bug，不应该在queryset里写filter。时间会提前算好，导致不准确
    serializer_class = DailyBoardSerializer
    filter_fields = ('username', 'collecttime')
    pagination_class = LimitOffsetPagination
    permission_classes = (ManagerOnly,)
    throttle_scope = "post"
    throttle_classes = [ScopedRateThrottle, ]


class TeamBoardView(viewsets.ModelViewSet):
    queryset = TeamBoard.objects.all()
    serializer_class = TeamBoardSerializer
    filter_fields = ('teammember', 'collecttime')
    pagination_class = LimitOffsetPagination
    permission_classes = (ManagerOnly,)
    throttle_scope = "post"
    throttle_classes = [ScopedRateThrottle, ]


class DailyContestBoardView(viewsets.ModelViewSet):
    queryset = DailyContestBoard.objects.all()
    serializer_class = DailyContestBoardSerializer
    filter_fields = ('contestdate', 'teammember')
    pagination_class = LimitOffsetPagination
    permission_classes = (ManagerOnly,)
    throttle_scope = "post"
    throttle_classes = [ScopedRateThrottle, ]
