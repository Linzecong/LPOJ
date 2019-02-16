# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination
from .models import JudgeStatus
from .serializers import JudgeStatusSerializer

class JudgeStatusView(viewsets.ModelViewSet):
    queryset = JudgeStatus.objects.all().order_by('-id')
    serializer_class = JudgeStatusSerializer
    pagination_class = LimitOffsetPagination
