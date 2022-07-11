<template>
  <div class="container">
    <h6 v-if="isSaving" class="d-inline-block mt-3">Сохранение...</h6>
    <h6 v-else class="d-inline-block mt-3">
      Сохранено
      <font-awesome-icon icon="fa-regular fa-circle-check" />
    </h6>
    <div
      v-if="testData"
      class="my-3 p-3 rounded-3 component-white-background test-data-top-border"
      style="position: relative"
    >
      <div
        class="d-flex flex-column border component-white-background rounded-3"
        style="position: absolute; right: -60px; top: 0px"
      >
        <button
          type="button"
          class="btn btn-light rounded-circle fs-6"
          @click="() => this.addNewQuestion(0)"
        >
          <font-awesome-icon icon="fa-solid fa-circle-plus" />
        </button>
      </div>
      <div class="my-3">
        <input
          type="text"
          class="form-control fs-2"
          v-model="testData.test_name"
        />
      </div>
      <div class="mb-3">
        <textarea
          v-model="testData.extra_data"
          class="form-control fs-6"
          rows="1"
          >{{ testData.extra_data }}
        </textarea>
      </div>
    </div>
    <div v-if="isQuestionListLoading"><Spinner /></div>
    <div v-else>
      <div v-if="questionList.length > 0">
        <div v-for="(question, index) in sortedQuestions" :key="question.id">
          <QuestionItem
            :question="question"
            @deleteQuestion="this.deleteQuestionHandler"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Spinner from "@/components/common/Spinner"
import QuestionItem from "@/components/psychotesting/QuestionItem"
import { mapGetters } from "vuex"
import { testDataAPI } from "@/api/testDataApi"
import { questionsAPI } from "@/api/questionsAPI"

export default {
  name: "TestQuestions",
  components: { Spinner, QuestionItem },
  data() {
    return {
      testData: null,
      questionList: [],
      isQuestionListLoading: true,
      isTestDataLoading: true,
      isSaving: false,
    }
  },
  computed: {
    ...mapGetters({
      userToken: "auth/getToken",
    }),
    sortedQuestions: function () {
      return this.questionList.sort(function (a, b) {
        return a - b
      })
    },
  },
  async created() {
    try {
      const response = await testDataAPI.getTestData(
        this.userToken,
        this.$route.params.id
      )
      const data = await response.data
      this.testData = data
      if (data) {
        const response = await questionsAPI.getQuestionsByTest(
          this.userToken,
          this.$route.params.id
        )
        const questions = await response.data
        this.questionList = questions
        this.isQuestionListLoading = false
      }
    } catch (e) {
    } finally {
      this.isTestDataLoading = false
    }
  },
  methods: {
    async updateTestData() {
      this.isSaving = true
      const response = await testDataAPI.updateTestData(
        this.userToken,
        this.testData
      )
      this.isSaving = false
    },
    async addNewQuestion(after) {
      this.isSaving = true
      const response = await questionsAPI.addNewQuestion(this.userToken, {
        test: this.testData.id,
        question_text: "Новый вопрос",
        question_type: 1,
        index_number: 1,
        is_active: true,
        has_required_answer: false,
        is_common_for_all_tests: false,
      })
      this.questionList.push(response.data)
      this.isSaving = false
    },
    async deleteQuestionHandler(questionId) {
      this.isSaving = true
      try {
        await questionsAPI.deleteQuestion(this.userToken, questionId)
      } catch (e) {
      } finally {
        this.questionList = this.questionList.filter(
          (question) => question.id !== questionId
        )
        this.isSaving = false
      }
    },
  },
  watch: {
    testData: {
      handler(newValue, oldValue) {
        this.updateTestData()
      },
      deep: true,
    },
  },
}
</script>

<style scoped></style>
