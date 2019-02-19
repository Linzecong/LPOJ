# -*- coding: utf-8 -*-

from rest_framework import serializers
from .models import ContestAnnouncement, ContestBoard, ContestComment, ContestInfo, ContestProblem, ContestRegister


class ContestAnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContestAnnouncement
        fields = '__all__'

class ContestBoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContestBoard
        fields = '__all__'

class ContestCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContestComment
        fields = '__all__'

class ContestInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContestInfo
        fields = '__all__'

class ContestProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContestProblem
        fields = '__all__'

class ContestRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContestRegister
        fields = '__all__'
    