# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from rest_framework import viewsets
from .models import JudgeStatus
from .serializers import JudgeStatusSerializer

class JudgeStatusView(viewsets.ModelViewSet):
    queryset = JudgeStatus.objects.all()
    serializer_class = JudgeStatusSerializer
