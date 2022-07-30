from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Organization, TestData, Question, AnswerSelectable, QuestionaryData, TestResult


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = '__all__'
        depth = 2


class TestDataSerializer(serializers.ModelSerializer):
    get_questions_count = serializers.ReadOnlyField()
    class Meta:
        model = TestData
        fields = '__all__'


class AnswerSelectableSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerSelectable
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSelectableSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['id','test', 'question_text', 'question_type', 'index_number', 'data_created', 'is_active',
                  'has_required_answer', 'is_common_for_all_tests', 'answers']


class QuestionaryDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionaryData
        fields = '__all__'


class TestResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestResult
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserNamesSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']
