from django.shortcuts import render
from rest_framework import viewsets
from .serializers import BoardSerializer,OthersSubmitSerializer,DailyBoardSerializer
from .permission import ManagerOnly
from .models import Board,OthersSubmit,DailyBoard
from rest_framework.pagination import LimitOffsetPagination
import datetime


class BoardView(viewsets.ModelViewSet):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    filter_fields = ('username',)
    pagination_class = LimitOffsetPagination
    permission_classes = (ManagerOnly,)

class DailyBoardView(viewsets.ModelViewSet):
    queryset = DailyBoard.objects.filter(collecttime__gte=datetime.datetime.now()-datetime.timedelta(days=30)).order_by('collecttime')
    serializer_class = DailyBoardSerializer
    filter_fields = ('username','collecttime')
    pagination_class = LimitOffsetPagination
    permission_classes = (ManagerOnly,)

class OthersSubmitView(viewsets.ModelViewSet):
    queryset = OthersSubmit.objects.all()
    serializer_class = OthersSubmitSerializer
    filter_fields = ('username','accepted')
    pagination_class = LimitOffsetPagination