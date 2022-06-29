from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework import permissions

from .models import Organization, TestData, Question, AnswerSelectable, QuestionaryData, TestResult
from .models import SINGLE, MULTIPLE, TEXT, SELECT, DATE
from .serializers import OrganizationSerializer, TestDataSerializer, QuestionSerializer, AnswerSelectableSerializer, \
    QuestionaryDataSerializer, TestResultSerializer


class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    # filterset_fields = {
    #     'owner_id': ['exact'],
    # }
    # permission_classes = [permissions.IsAuthenticated]


class TestDataViewSet(viewsets.ModelViewSet):
    queryset = TestData.objects.all()
    serializer_class = TestDataSerializer


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
