from django.shortcuts import render
from rest_framework import viewsets
from .serializers import WikiSerializer,WikiCountSerializer
from .permission import UserOnly
from .models import Wiki
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