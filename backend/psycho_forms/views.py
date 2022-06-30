from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.contrib.auth.hashers import make_password

from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework import permissions

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

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    filterset_fields = {
        'test_id': ['exact'],
    }


class AnswerSelectableViewSet(viewsets.ModelViewSet):
    queryset = AnswerSelectable.objects.all()
    serializer_class = AnswerSelectableSerializer


class QuestionaryDataViewSet(viewsets.ModelViewSet):
    queryset = QuestionaryData.objects.all()
    serializer_class = QuestionaryDataSerializer


class TestResultViewSet(viewsets.ModelViewSet):
    queryset = TestResult.objects.all()
    serializer_class = TestResultSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


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

