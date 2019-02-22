# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from rest_framework import viewsets, mixins
from rest_framework.pagination import LimitOffsetPagination
from .models import JudgeStatus
from .serializers import JudgeStatusSerializer
from .permission import LoginOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.throttling import ScopedRateThrottle

class JudgeStatusView(viewsets.ModelViewSet):
    queryset = JudgeStatus.objects.all().order_by('-id')
    serializer_class = JudgeStatusSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('user', 'result', "contest")
    permission_classes = (LoginOrReadOnly,)

class JudgeStatusPutView(viewsets.GenericViewSet, mixins.CreateModelMixin):
    queryset = JudgeStatus.objects.all()
    serializer_class = JudgeStatusSerializer
    permission_classes = (LoginOrReadOnly,)
    throttle_scope  = "judge"
    throttle_classes =[ScopedRateThrottle,]