# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from rest_framework import viewsets
from .models import Problem,ProblemData,ProblemTag
from .serializers import ProblemSerializer,ProblemDataSerializer,ProblemTagSerializer
from rest_framework.pagination import LimitOffsetPagination


class ProblemView(viewsets.ModelViewSet):
    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer

class ProblemDataView(viewsets.ModelViewSet):
    queryset = ProblemData.objects.all()
    serializer_class = ProblemDataSerializer
    pagination_class = LimitOffsetPagination

class ProblemTagView(viewsets.ModelViewSet):
    queryset = ProblemTag.objects.all()
    serializer_class = ProblemTagSerializer
