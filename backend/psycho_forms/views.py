from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

from rest_framework import viewsets
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from jose import jwt

from .models import Organization, TestData, Question, AnswerSelectable, QuestionaryData, TestResult
from .models import SINGLE, MULTIPLE, TEXT, SELECT, DATE
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
    permission_classes = [permissions.IsAuthenticated]


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    filterset_fields = {
        'test_id': ['exact'],
    }
    permission_classes = [permissions.IsAuthenticated]


class AnswerSelectableViewSet(viewsets.ModelViewSet):
    queryset = AnswerSelectable.objects.all()
    serializer_class = AnswerSelectableSerializer
    permission_classes = [permissions.IsAuthenticated]


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


# signal
@receiver(post_save, sender=User)
def user_post_save_handler(sender, instance, created, **kwargs):
    if isinstance(instance, User):
        if created:
            Organization.objects.create(user=instance, organization_name="Без названия")


# @receiver(post_save, sender=Question)
# def question_post_save_handler(sender, instance, created, **kwargs):
#     if isinstance(instance, Question):
#         if created:
#             AnswerSelectable.objects.create(question=instance, answer_text="Новый ответ", index_number=1)


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
