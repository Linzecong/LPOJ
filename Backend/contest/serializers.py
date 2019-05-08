# -*- coding: utf-8 -*-
from rest_framework import serializers
from .models import ContestAnnouncement,ContestTutorial, ContestComingInfo, ContestRank, ContestRatingChange, ContestBoard, ContestComment, ContestInfo, ContestProblem, ContestRegister


class ContestAnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContestAnnouncement
        fields = '__all__'

class ContestTutorialSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContestTutorial
        fields = '__all__'


class ContestBoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContestBoard
        fields = '__all__'


class ContestRankSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContestRank
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


class ContestRatingChangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContestRatingChange
        fields = '__all__'


class ContestComingInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContestComingInfo
        fields = '__all__'
