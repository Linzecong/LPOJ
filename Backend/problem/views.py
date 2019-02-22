# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from rest_framework import viewsets, mixins
from .models import Problem, ProblemData, ProblemTag
from .serializers import ProblemSerializer, ProblemDataSerializer, ProblemTagSerializer
from .permission import ManagerOnly, AuthOnly
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend

class ProblemView(viewsets.GenericViewSet, mixins.DestroyModelMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin):
    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer
    filter_fields = ('auth',)
    permission_classes = (AuthOnly,)


class ProblemDataView(viewsets.ModelViewSet):
    queryset = ProblemData.objects.all()
    serializer_class = ProblemDataSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (ManagerOnly,)
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('auth',)


class ProblemTagView(viewsets.ModelViewSet):
    queryset = ProblemTag.objects.all()
    serializer_class = ProblemTagSerializer
    permission_classes = (ManagerOnly,)
