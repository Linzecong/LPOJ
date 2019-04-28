# -*- coding: utf-8 -*-
from rest_framework import serializers
from .models import Board, DailyBoard, TeamBoard, DailyContestBoard


class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = '__all__'


class DailyBoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyBoard
        fields = '__all__'


class TeamBoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamBoard
        fields = '__all__'


class DailyContestBoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyContestBoard
        fields = '__all__'
