# -*- coding: utf-8 -*-
from rest_framework import serializers
from .models import Classes
from .models import ClassStudentData
class ClassDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classes
        fields = '__all__'

class ClassStudentDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassStudentData
        fields = '__all__'
