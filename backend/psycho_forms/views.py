from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.db.models import F
from django.core.exceptions import ValidationError
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.decorators import action

from jose import jwt

from .models import Organization, TestData, Question, AnswerSelectable, QuestionaryData, TestResult
from .models import SINGLE, MULTIPLE, TEXT, DATE, SELECT
from .serializers import OrganizationSerializer, TestDataSerializer, QuestionSerializer, AnswerSelectableSerializer, \
    QuestionaryDataSerializer, TestResultSerializer, UserSerializer

from datetime import date


class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    filterset_fields = {
        'user_id': ['exact'],
    }
    permission_classes = [permissions.IsAuthenticated]


class TestDataViewSet(viewsets.ModelViewSet):
    queryset = TestData.objects.all()
    serializer_class = TestDataSerializer
    filterset_fields = {
        'organization_id': ['exact'],
    }
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        new_test = serializer.save()
        if 'after' in self.request.query_params:
            new_test.index_number = int(self.request.query_params['after']) + 1
            new_test.save()

    def perform_destroy(self, instance):
        instance.delete()
        organization = get_object_or_404(Organization, pk=instance.organization.id)
        if instance.index_number:
            organization.testdata_set.filter(index_number__gt=instance.index_number).update(
                index_number=F('index_number') - 1)

    @action(detail=True, methods=['post'])
    @transaction.atomic
    def make_copy(self, request, pk=None):
        test_data = get_object_or_404(TestData, pk=pk)
        organization = get_object_or_404(Organization, pk=test_data.organization.id)
        organization.testdata_set.filter(index_number__gt=test_data.index_number).update(
            index_number=F('index_number') + 1)
        try:
            copy_test = TestData.objects.create(organization=organization,
                                                test_name=test_data.test_name + ' (копия)',
                                                extra_data=test_data.extra_data,
                                                is_active=test_data.is_active,
                                                index_number=test_data.index_number + 1
                                                )
            for question in test_data.question_set.all():
                copy_question = Question.objects.create(test=copy_test,
                                                        question_type=question.question_type,
                                                        question_text=question.question_text,
                                                        index_number=question.index_number,
                                                        is_active=question.is_active,
                                                        has_required_answer=question.has_required_answer,
                                                        is_common_for_all_tests=question.is_common_for_all_tests
                                                        )
                for answer in question.answers.all():
                    AnswerSelectable.objects.create(question=copy_question,
                                                    answer_text=answer.answer_text,
                                                    has_extra_data=answer.has_extra_data,
                                                    index_number=answer.index_number)
        except ValidationError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(TestDataSerializer(copy_test).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def results_full_text(self, request, pk=None):
        response_results_list = []
        test_data = get_object_or_404(TestData, pk=pk)
        result_list_all = TestResult.objects.filter(questionary_data__test=test_data)
        for questionary in QuestionaryData.objects.all():
            result_dict = {'date': str(questionary.data_created.date())}
            for question in test_data.question_set.all():
                question_results = result_list_all.filter(questionary_data=questionary, question=question)
                res_str = ''
                if question_results.count() > 0:
                    for q_r in question_results:
                        if q_r.answer_selectable:
                            res_str = res_str + str(q_r.answer_selectable)
                            res_str += '; '
                        if q_r.answer_text:
                            res_str = res_str + str(q_r.answer_text)
                            res_str += '; '
                        if q_r.answer_date:
                            res_str = res_str + str(q_r.answer_date)
                            res_str += '; '
                        if q_r.extra_data:
                            res_str += 'пояснение к ответу - '
                            res_str = res_str + str(q_r.extra_data)
                            res_str += '; '
                result_dict[question.id] = res_str
            response_results_list.append(result_dict)
        return Response(response_results_list, status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def results_answers_count(self, request, pk=None):
        response_results_dict = {}
        test_data = get_object_or_404(TestData, pk=pk)
        result_list_all = TestResult.objects.filter(questionary_data__test=test_data)

        for question in test_data.question_set.all():
            if question.question_type in [SINGLE, MULTIPLE, SELECT]:
                for answer in question.answers.all():
                    response_results_dict[answer.id] = result_list_all.filter(answer_selectable=answer).count()
        return Response(response_results_dict, status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def results_answers_1_0(self, request, pk=None):
        response_results_list = []
        test_data = get_object_or_404(TestData, pk=pk)
        result_list_all = TestResult.objects.filter(questionary_data__test=test_data)
        for questionary in QuestionaryData.objects.all():
            result_dict = {'date': str(questionary.data_created.date())}
            for question in test_data.question_set.all():
                question_results = result_list_all.filter(questionary_data=questionary, question=question)
                for answer in question.answers.all():
                    if question_results.filter(answer_selectable=answer).count() > 0:
                        result_dict[answer.id] = '1'
                    else:
                        result_dict[answer.id] = '0'
            response_results_list.append(result_dict)
        return Response(response_results_list, status.HTTP_200_OK)


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    filterset_fields = {
        'test_id': ['exact'],
    }
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(detail=True, methods=['post'])
    @transaction.atomic
    def make_copy(self, request, pk=None):
        question = get_object_or_404(Question, pk=pk)
        test_data = get_object_or_404(TestData, pk=question.test.id)
        test_data.question_set.filter(index_number__gt=question.index_number).update(
            index_number=F('index_number') + 1)
        try:
            copy_question = Question.objects.create(test=test_data,
                                                    question_type=question.question_type,
                                                    question_text=question.question_text + ' (копия)',
                                                    is_active=question.is_active,
                                                    has_required_answer=question.has_required_answer,
                                                    is_common_for_all_tests=question.is_common_for_all_tests,
                                                    index_number=question.index_number + 1
                                                    )
            for answer in question.answers.all():
                AnswerSelectable.objects.create(question=copy_question,
                                                answer_text=answer.answer_text,
                                                has_extra_data=answer.has_extra_data,
                                                index_number=answer.index_number)
        except ValidationError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(QuestionSerializer(copy_question).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def delete_all_answers(self, request, pk=None):
        question = get_object_or_404(Question, pk=pk)
        question.answers.all().delete()
        return Response(QuestionSerializer(question).data, status=status.HTTP_200_OK)

    def perform_create(self, serializer):
        new_question = serializer.save()
        if 'after' in self.request.query_params:
            test_data = get_object_or_404(TestData, pk=new_question.test.id)
            test_data.question_set.filter(index_number__gt=int(self.request.query_params['after'])).update(index_number=F('index_number') + 1)
            new_question.index_number = int(self.request.query_params['after']) + 1
            new_question.save()
        AnswerSelectable.objects.create(question=new_question, answer_text='Новый ответ', index_number=1)

    def perform_destroy(self, instance):
        instance.delete()
        test_data = get_object_or_404(TestData, pk=instance.test.id)
        if instance.index_number:
            test_data.question_set.filter(index_number__gt=instance.index_number).update(
                index_number=F('index_number') - 1)


class AnswerSelectableViewSet(viewsets.ModelViewSet):
    queryset = AnswerSelectable.objects.all()
    serializer_class = AnswerSelectableSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        new_answer = serializer.save()
        question = get_object_or_404(Question, pk=new_answer.question.id)
        answer_list = question.answers.all()
        new_answer.index_number = answer_list.count()
        new_answer.save()

    def perform_destroy(self, instance):
        instance.delete()
        question = get_object_or_404(Question, pk=instance.question.id)
        question.answers.filter(index_number__gt=instance.index_number).update(index_number=F('index_number') - 1)


class QuestionaryDataViewSet(viewsets.ModelViewSet):
    queryset = QuestionaryData.objects.all()
    serializer_class = QuestionaryDataSerializer
    permission_classes = [permissions.IsAuthenticated]


class TestResultViewSet(viewsets.ModelViewSet):
    queryset = TestResult.objects.all()
    serializer_class = TestResultSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_me(request):
    try:
        token = request.META['HTTP_AUTHORIZATION'].split(" ")[1]
        payload = jwt.decode(token, key=settings.SIMPLE_JWT['SIGNING_KEY'], algorithms=['HS256'])
    except jwt.JWTError:
        return Response(status=status.HTTP_403_FORBIDDEN)
    try:
        user_data = Organization.objects.get(user_id=payload['user_id'])
        serializer = OrganizationSerializer(user_data)
        return Response(serializer.data)
    except Organization.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    except Exception:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@transaction.atomic
def save_test_running_data(request):
    current_test = get_object_or_404(TestData, pk=request.data['test_id'])
    new_questionary_data = QuestionaryData(
        test=current_test,
    )
    new_questionary_data.save()

    for question in current_test.question_set.all():
        if question.question_type == SINGLE:
            if 'question_' + str(question.id) + '_radio' in request.POST:
                answer = get_object_or_404(AnswerSelectable, pk=request.POST[
                    'question_' + str(question.id) + '_radio'])
                new_result = TestResult.objects.create(
                    questionary_data=new_questionary_data,
                    question=question,
                    answer_selectable=answer
                )
                if answer.has_extra_data:
                    if 'question_' + str(question.id) + '_radio_extra_input' in request.POST:
                        new_result.extra_data = request.POST['question_' + str(question.id) + '_radio_extra_input']
                        new_result.save()
        elif question.question_type == MULTIPLE:
            for i in range(question.answers.all().count()):
                if 'question_' + str(question.id) + '_checkbox_' + str(i) in request.POST:
                    answer = get_object_or_404(AnswerSelectable, pk=request.POST[
                        'question_' + str(question.id) + '_checkbox_' + str(i)])
                    new_result = TestResult.objects.create(
                        questionary_data=new_questionary_data,
                        question=question,
                        answer_selectable=answer
                    )
                    if answer.has_extra_data:
                        if 'question_' + str(question.id) + '_checkbox_' + str(i) + '_extra_input' in request.POST:
                            new_result.extra_data = request.POST[
                                'question_' + str(question.id) + '_checkbox_' + str(i) + '_extra_input']
                            new_result.save()
        elif question.question_type == SELECT:
            if 'question_' + str(question.id) + '_select' in request.POST:
                answer = get_object_or_404(AnswerSelectable, pk=request.POST[
                    'question_' + str(question.id) + '_select'])
                new_test_result = TestResult(
                    questionary_data=new_questionary_data,
                    question=question,
                    answer_selectable=answer
                )
                new_test_result.save()
        elif question.question_type == TEXT:
            if 'question_' + str(question.id) + '_text' in request.POST:
                new_test_result = TestResult(
                    questionary_data=new_questionary_data,
                    question=question,
                    answer_text=request.POST['question_' + str(question.id) + '_text']
                )
                new_test_result.save()
        elif question.question_type == DATE:
            if 'question_' + str(question.id) + '_date' in request.POST:
                serializer = TestResultSerializer(
                    data={'questionary_data': new_questionary_data.id, 'question': question.id,
                          'answer_date': request.POST['question_' + str(question.id) + '_date']})
                if serializer.is_valid():
                    new_test_result = TestResult(
                        questionary_data=new_questionary_data,
                        question=question,
                        answer_date=request.POST['question_' + str(question.id) + '_date']
                    )
                    new_test_result.save()
        else:
            pass
    return Response(status=status.HTTP_200_OK)


# signal
@receiver(post_save, sender=User)
def user_post_save_handler(sender, instance, created, **kwargs):
    if isinstance(instance, User):
        if created:
            Organization.objects.create(user=instance, organization_name="Без названия")
