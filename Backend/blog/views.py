from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.throttling import ScopedRateThrottle
from .models import OJMessage, Blog
from .serializers import OJMessageSerializer, BlogSerializer
from .permission import ManagerOnly, UserRatingOnly


class OJMessageView(viewsets.ModelViewSet):
    queryset = OJMessage.objects.all().order_by("-id")
    serializer_class = OJMessageSerializer
    filter_fields = ('username', 'time')
    permission_classes = (UserRatingOnly,)
    pagination_class = LimitOffsetPagination
    throttle_scope = "post"
    throttle_classes = [ScopedRateThrottle, ]


class BlogView(viewsets.ModelViewSet):
    queryset = Blog.objects.all().order_by("-id")
    serializer_class = BlogSerializer
    filter_fields = ('username', 'time')
    pagination_class = LimitOffsetPagination
    permission_classes = (ManagerOnly,)
    throttle_scope = "post"
    throttle_classes = [ScopedRateThrottle, ]
