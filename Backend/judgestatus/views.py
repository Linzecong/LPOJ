# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination
from .models import JudgeStatus
from .serializers import JudgeStatusSerializer
from django_filters.rest_framework import DjangoFilterBackend

class JudgeStatusView(viewsets.ModelViewSet):
    queryset = JudgeStatus.objects.all().order_by('-id')
    serializer_class = JudgeStatusSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('user', 'result', "contest")
