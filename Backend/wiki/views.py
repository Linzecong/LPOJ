from django.shortcuts import render
from rest_framework import viewsets
from .serializers import WikiSerializer,WikiCountSerializer,MBCodeSerializer,MBCodeDetailSerializer,MBCodeDetailNoCodeSerializer
from .permission import UserOnly
from .models import Wiki,MBCode,MBCodeDetail
from rest_framework.throttling import ScopedRateThrottle

# Create your views here.
class WikiView(viewsets.ModelViewSet):
    queryset = Wiki.objects.all()
    serializer_class = WikiSerializer
    filter_fields = ('username','type')
    permission_classes = (UserOnly,)
    throttle_scope  = "post"
    throttle_classes =[ScopedRateThrottle,]

class WikiCountView(viewsets.ModelViewSet):
    queryset = Wiki.objects.all()
    serializer_class = WikiCountSerializer
    filter_fields = ('username','type')
    permission_classes = (UserOnly,)
    throttle_scope  = "post"
    throttle_classes =[ScopedRateThrottle,]

class MBCodeView(viewsets.ModelViewSet):
    queryset = MBCode.objects.all()
    serializer_class = MBCodeSerializer
    filter_fields = ('username',)
    permission_classes = (UserOnly,)
    throttle_scope  = "post"
    throttle_classes =[ScopedRateThrottle,]

class MBCodeDetailView(viewsets.ModelViewSet):
    queryset = MBCodeDetail.objects.all()
    serializer_class = MBCodeDetailSerializer
    filter_fields = ('username','group','des','title')
    permission_classes = (UserOnly,)
    throttle_scope  = "post"
    throttle_classes =[ScopedRateThrottle,]

class MBCodeDetailNoCodeView(viewsets.ModelViewSet):
    queryset = MBCodeDetail.objects.all()
    serializer_class = MBCodeDetailNoCodeSerializer
    filter_fields = ('username','group','des','title')
    permission_classes = (UserOnly,)
    throttle_scope  = "post"
    throttle_classes =[ScopedRateThrottle,]