<template>
  <div
    v-if="isLoading"
    class="d-flex justify-content-center align-items-center"
    style="height: 70vh"
  >
    <Spinner />
  </div>
  <div v-else class="container">
    <div
      class="my-3 p-3 rounded-3 component-white-background test-data-top-border"
      v-if="testData"
    >
      <h1>{{ testData.test_name }}</h1>
      <h3>{{ testData.extra_data }}</h3>
    </div>
    <div v-if="this.questionList.length > 0">
      <form @submit="submitForm" method="POST">

        <div v-for="question in sortedQuestions" :key="question.id">
          <QuestionItemRunning :question="question" />
        </div>



<!--        <div-->
<!--          v-for="question in sortedQuestions"-->
<!--          :key="question.id"-->
<!--          class="my-3 p-3 rounded-3 component-white-background component-left-border"-->
<!--        >-->
<!--          <h5>{{ question.question_text }}</h5>-->
<!--          <div v-if="question.question_type === this.questionTypes['RADIO']">-->
<!--            <div class="form-check" v-for="answer in question.answers">-->
<!--              <input-->
<!--                class="form-check-input"-->
<!--                type="radio"-->
<!--                name="flexRadioDefault"-->
<!--                id="flexRadioDefault1"-->
<!--              />-->
<!--              <label class="form-check-label" for="flexRadioDefault1">-->
<!--                {{ answer.answer_text }}-->
<!--              </label>-->
<!--            </div>-->
<!--          </div>-->
<!--        </div>-->
        <button type="submit" class="btn btn-primary">Отправить</button>
      </form>
    </div>
  </div>
</template>

<script>
import Spinner from "@/components/common/Spinner"
import QuestionItemRunning from "@/components/psychotesting/running/QuestionItemRunning"
import { testDataAPI } from "@/api/testDataApi"
import { questionsAPI } from "@/api/questionsAPI"
import questionTypes from "@/components/psychotesting/questionTypes"
import axios from "axios"

export default {
  name: "TestRunning",
  components: { Spinner, QuestionItemRunning },
  data() {
    return {
      testData: null,
      questionList: [],
      questionTypes: questionTypes,
      isLoading: false,
      isError: false,
      resultData: {},
    }
  },
  methods: {
    submitForm(e) {
      e.preventDefault()
      const formData = new FormData(e.target)
      const obj = {}
      for (let key of formData.keys()) {
        obj[key] = formData.get(key)
      }
      console.log(obj)
      axios.post(
        `${process.env.VUE_APP_BACKEND_PROTOCOL}://${process.env.VUE_APP_BACKEND_HOST}:${process.env.VUE_APP_BACKEND_PORT}/api/test-running/save/`,
        new FormData(e.target)
      )
      // console.log(new FormData(e.target))
    },
  },
  computed: {
    sortedQuestions: function () {
      return this.questionList.sort(function (a, b) {
        if (a.index_number < b.index_number) {
          return -1
        }
        if (a.index_number > b.index_number) {
          return 1
        }
        return 0
      })
    },
  },
  async created() {
    try {
      const response = await testDataAPI.getTestDataForRunning(
        this.$route.params.id
      )
      const data = await response.data
      this.testData = data
      if (data) {
        const response = await questionsAPI.getQuestionsByTestForRunning(
          this.$route.params.id
        )
        this.questionList = await response.data
      }
    } catch (e) {
      this.isError = true
    } finally {
      this.isLoading = false
    }
  },
}
</script>

<style scoped></style>
