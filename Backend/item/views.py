# -*- coding: utf-8 -*-
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.hashers import make_password, check_password
from rest_framework import viewsets,filters,generics,mixins
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.throttling import ScopedRateThrottle
from .models import Item
from .serializers import ItemSerializer
from .permission import UserOnly
from board.models import SettingBoard


def getWikiPermission():
    setting = SettingBoard.objects.filter(id=1)
    if len(setting) != 0:
        if setting[0].openwiki is False:
            return False
        else:
            return True
    else:
        return False

class ItemPutView(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = (UserOnly,)

class ItemGetAPIView(generics.GenericAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = (AllowAny,)

    def get(self, request, format=None):
        if getWikiPermission() == False:
            return Response("not open!", HTTP_400_BAD_REQUEST)
        username = request.session.get('user_id', None)
        user = Item.objects.filter(user=username)
        serializer = ItemSerializer(user, many=True)
        return Response(serializer.data, HTTP_200_OK)
        