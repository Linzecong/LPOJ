# -*- coding: utf-8 -*-

from rest_framework import serializers
from .models import JudgeStatus

class JudgeStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = JudgeStatus
        fields = '__all__'
    
    