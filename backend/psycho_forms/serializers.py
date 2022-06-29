from rest_framework import serializers
from .models import Organization, TestData, Question, AnswerSelectable, QuestionaryData, TestResult
from django.contrib.auth.models import User


class OrganizationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Organization
        fields = '__all__'


class TestDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = TestData
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = '__all__'


class AnswerSelectableSerializer(serializers.ModelSerializer):

    class Meta:
        model = AnswerSelectable
        fields = '__all__'


class QuestionaryDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = QuestionaryData
        fields = '__all__'


class TestResultSerializer(serializers.ModelSerializer):

    class Meta:
        model = TestResult
        fields = '__all__'