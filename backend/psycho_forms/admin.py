from django.contrib import admin
from .models import QuestionaryData, Question, AnswerSelectable, Organization, TestResult, TestData

admin.site.register(TestData)
admin.site.register(QuestionaryData)
admin.site.register(Question)
admin.site.register(AnswerSelectable)
admin.site.register(Organization)
admin.site.register(TestResult)