from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.decorators import action

from jose import jwt

from .models import Organization, TestData, Question, AnswerSelectable, QuestionaryData, TestResult
from .serializers import OrganizationSerializer, TestDataSerializer, QuestionSerializer, AnswerSelectableSerializer, \
    QuestionaryDataSerializer, TestResultSerializer, UserSerializer


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

    @action(detail=True, methods=['post'])
    def make_copy(self, request, pk=None):
        test_data = get_object_or_404(TestData, pk=pk)
        organization = get_object_or_404(Organization, pk=test_data.organization.id)
        copy_test = TestData.objects.create(organization=organization,
                                            test_name=test_data.test_name,
                                            extra_data=test_data.extra_data,
                                            is_active=test_data.is_active
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

        return Response(TestDataSerializer(copy_test).data, status=status.HTTP_201_CREATED)


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    filterset_fields = {
        'test_id': ['exact'],
    }
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(detail=True, methods=['post'])
    def make_copy(self, request, pk=None):
        try:
            question = get_object_or_404(Question, pk=pk)
            test_data = get_object_or_404(TestData, pk=question.test.id)
            copy_question = Question.objects.create(test=test_data,
                                                    question_type=question.question_type,
                                                    question_text=question.question_text,
                                                    is_active=question.is_active,
                                                    has_required_answer=question.has_required_answer,
                                                    is_common_for_all_tests=question.is_common_for_all_tests)
            question_list_after = test_data.question_set.filter(index_number__gt=question.index_number)

            for quest in question_list_after:
                quest.index_number = quest.index_number + 1
                quest.save()
            copy_question.index_number = question.index_number + 1
            copy_question.save()

            for answer in question.answers.all():
                AnswerSelectable.objects.create(question=copy_question,
                                                answer_text=answer.answer_text,
                                                has_extra_data=answer.has_extra_data,
                                                index_number=answer.index_number)

            return Response(QuestionSerializer(copy_question).data, status=status.HTTP_201_CREATED)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def delete_all_answers(self, request, pk=None):
        try:
            question = get_object_or_404(Question, pk=pk)
            question.answers.all().delete()
            return Response(QuestionSerializer(question).data, status=status.HTTP_200_OK)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        new_question = serializer.save()
        if 'after' in self.request.query_params:
            after = self.request.query_params['after']
            test_data = get_object_or_404(TestData, pk=new_question.test.id)
            question_list_after = test_data.question_set.filter(index_number__gt=after)
            for question in question_list_after:
                question.index_number = question.index_number + 1
                question.save()
            new_question.index_number = int(self.request.query_params['after']) + 1
            new_question.save()
        else:
            new_question.index_number = 1
            new_question.save()
        AnswerSelectable.objects.create(question=new_question, answer_text='Новый ответ', index_number=1)

    def perform_destroy(self, instance):
        instance.delete()
        test_data = get_object_or_404(TestData, pk=instance.test.id)
        if instance.index_number:
            question_list_after = test_data.question_set.filter(index_number__gt=instance.index_number)
            for question in question_list_after:
                question.index_number = question.index_number - 1
                question.save()


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
        answer_list_after = question.answers.filter(index_number__gt=instance.index_number)
        for answer in answer_list_after:
            answer.index_number = answer.index_number - 1
            answer.save()


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
def save_test_running_data(request):
    print(request.data)
    print('save')


# signal
@receiver(post_save, sender=User)
def user_post_save_handler(sender, instance, created, **kwargs):
    if isinstance(instance, User):
        if created:
            Organization.objects.create(user=instance, organization_name="Без названия")


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
        })
