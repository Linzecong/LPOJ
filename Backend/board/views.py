from django.shortcuts import render
from rest_framework import viewsets
from .serializers import BoardSerializer,OthersSubmitSerializer,DailyBoardSerializer,TeamBoardSerializer,DailyContestBoardSerializer
from .permission import ManagerOnly
from .models import Board,OthersSubmit,DailyBoard,TeamBoard,DailyContestBoard
from rest_framework.pagination import LimitOffsetPagination
import datetime
from rest_framework.throttling import ScopedRateThrottle

class BoardView(viewsets.ModelViewSet):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    filter_fields = ('username',)
    pagination_class = LimitOffsetPagination
    permission_classes = (ManagerOnly,)
    throttle_scope  = "post"
    throttle_classes =[ScopedRateThrottle,]

class DailyBoardView(viewsets.ModelViewSet):
    queryset = DailyBoard.objects.filter(collecttime__gte=datetime.datetime.now()-datetime.timedelta(days=10)).order_by('collecttime')
    serializer_class = DailyBoardSerializer
    filter_fields = ('username','collecttime')
    pagination_class = LimitOffsetPagination
    permission_classes = (ManagerOnly,)
    throttle_scope  = "post"
    throttle_classes =[ScopedRateThrottle,]

class OthersSubmitView(viewsets.ModelViewSet):
    queryset = OthersSubmit.objects.all()
    serializer_class = OthersSubmitSerializer
    filter_fields = ('username','accepted')
    pagination_class = LimitOffsetPagination
    throttle_scope  = "post"
    throttle_classes =[ScopedRateThrottle,]

class TeamBoardView(viewsets.ModelViewSet):
    queryset = TeamBoard.objects.all()
    serializer_class = TeamBoardSerializer
    filter_fields = ('teammember','collecttime')
    pagination_class = LimitOffsetPagination
    permission_classes = (ManagerOnly,)
    throttle_scope  = "post"
    throttle_classes =[ScopedRateThrottle,]

class DailyContestBoardView(viewsets.ModelViewSet):
    queryset = DailyContestBoard.objects.all()
    serializer_class = DailyContestBoardSerializer
    filter_fields = ('contestdate','teammember')
    pagination_class = LimitOffsetPagination
    permission_classes = (ManagerOnly,)
    throttle_scope  = "post"
    throttle_classes =[ScopedRateThrottle,]
