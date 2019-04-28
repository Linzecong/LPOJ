# -*- coding: utf-8 -*-

from rest_framework import serializers
from .models import JudgeStatus, CaseStatus


class JudgeStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = JudgeStatus
        exclude = ['code']


class JudgeStatusCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = JudgeStatus
        fields = '__all__'


class CaseStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = CaseStatus
        fields = '__all__'
