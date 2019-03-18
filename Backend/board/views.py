from django.shortcuts import render
from rest_framework import viewsets
from .serializers import BoardSerializer,OthersSubmitSerializer
from .permission import ManagerOnly
from .models import Board,OthersSubmit
from rest_framework.pagination import LimitOffsetPagination



class BoardView(viewsets.ModelViewSet):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    filter_fields = ('username',)
    pagination_class = LimitOffsetPagination
    permission_classes = (ManagerOnly,)

class OthersSubmitView(viewsets.ModelViewSet):
    queryset = OthersSubmit.objects.all()
    serializer_class = OthersSubmitSerializer
    filter_fields = ('username','accepted')
    pagination_class = LimitOffsetPagination