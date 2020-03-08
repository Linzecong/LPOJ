# -*- coding: utf-8 -*-
from rest_framework import serializers
from .models import Problem, ProblemData, ProblemTag,ChoiceProblem


class ProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = '__all__'

class ChoiceProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChoiceProblem
        fields = '__all__'


class ProblemDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProblemData
        fields = '__all__'


class ProblemTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProblemTag
        fields = '__all__'

