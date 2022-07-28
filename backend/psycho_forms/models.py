from django.db import models
from django.contrib.auth.models import User

SINGLE = 1
MULTIPLE = 2
TEXT = 3
SELECT = 4
DATE = 5

QUESTION_TYPE_CHOICES = (
    (SINGLE, 'Single (radio)'),
    (MULTIPLE, 'Multiple (checkbox)'),
    (TEXT, 'Text field'),
    (SELECT, 'Select field'),
    (DATE, 'Date field'),
)


class Organization(models.Model):
    user = models.OneToOneField(User, verbose_name="Пользователь", on_delete=models.CASCADE)
    organization_name = models.CharField(verbose_name="Название организации", max_length=255, default="Без названия")
    data_created = models.DateTimeField(verbose_name="Дата и время создания", auto_now_add=True)

    def __str__(self):
        return self.organization_name

    class Meta:
        ordering = ('id',)
        verbose_name = 'Organization'
        verbose_name_plural = 'Organizations'


class TestData(models.Model):
    organization = models.ForeignKey(Organization, verbose_name="Организация(владелец теста)", on_delete=models.CASCADE)
    test_name = models.CharField(verbose_name="Название теста", max_length=255)
    extra_data = models.TextField(verbose_name="Дополнительная информация", blank=True, null=True)
    index_number = models.IntegerField(verbose_name="Порядковый номер теста", blank=True, null=True)
    introduction = models.TextField(verbose_name="Вступительный текст", blank=True, null=True)
    data_created = models.DateTimeField(verbose_name="Дата и время создания", auto_now_add=True)
    is_active = models.BooleanField(verbose_name="Является активным", default=True)

    @property
    def get_questions_count(self):
        return self.question_set.all().count()

    def __str__(self):
        return self.test_name

    class Meta:
        ordering = ('id',)
        verbose_name = 'TestData'
        verbose_name_plural = '1 TestsData'


class Question(models.Model):
    test = models.ForeignKey(TestData, on_delete=models.CASCADE, verbose_name="Тест")
    question_type = models.IntegerField(verbose_name="Тип вопроса", choices=QUESTION_TYPE_CHOICES, default=SINGLE)
    question_text = models.TextField(verbose_name="Текст вопроса")
    index_number = models.IntegerField(verbose_name="Порядковый номер вопроса", blank=True, null=True)
    data_created = models.DateTimeField(verbose_name="Дата и время создания", auto_now_add=True)
    is_active = models.BooleanField(verbose_name="Является активным", default=True)
    has_required_answer = models.BooleanField(verbose_name="Ответ на данный вопрос обязателен", default=True)
    is_common_for_all_tests = models.BooleanField(verbose_name="Является общим для всех тестов", default=False)

    def __str__(self):
        return self.question_text + ' ' + str(self.question_type)

    class Meta:
        ordering = ('index_number',)
        verbose_name = 'Question'
        verbose_name_plural = '2 Questions'


class AnswerSelectable(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers', verbose_name="Вопрос")
    answer_text = models.TextField(verbose_name="Текст ответа")
    has_extra_data = models.BooleanField(verbose_name="Имеет дополнительную информацию", default=False)
    index_number = models.IntegerField(verbose_name="Порядковый номер ответа", blank=True, null=True)

    def __str__(self):
        return self.answer_text

    class Meta:
        ordering = ('id',)
        verbose_name = 'Answer'
        verbose_name_plural = '3 Answers'


class QuestionaryData(models.Model):
    test = models.ForeignKey(TestData, verbose_name="Тест", on_delete=models.CASCADE, blank=True, null=True)
    data_created = models.DateTimeField(verbose_name="Дата и время прохождения теста", auto_now_add=True)
    extra_data = models.TextField(verbose_name="Дополнительная информация", blank=True, null=True)

    def __str__(self):
        return self.test.test_name + ' ' + str(self.data_created)

    class Meta:
        ordering = ('id',)
        verbose_name = 'QuestionaryData'
        verbose_name_plural = 'QuestionaryData'


class TestResult(models.Model):
    questionary_data = models.ForeignKey(QuestionaryData, on_delete=models.CASCADE, verbose_name="Данные анкеты")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name="Вопрос")
    answer_selectable = models.ForeignKey(AnswerSelectable, on_delete=models.CASCADE, verbose_name="Ответ(выбираемый)",
                                          blank=True, null=True)
    answer_text = models.TextField(verbose_name="Ответ (текстовый)", blank=True, null=True)
    answer_date = models.DateField(verbose_name="Ответ (дата)", blank=True, null=True)
    extra_data = models.TextField(verbose_name="Дополнительная информация к ответу", blank=True, null=True)

    def __str__(self):
        return str(self.questionary_data)

    class Meta:
        ordering = ('id',)
        verbose_name = 'TestResult'
        verbose_name_plural = '4 TestResults'