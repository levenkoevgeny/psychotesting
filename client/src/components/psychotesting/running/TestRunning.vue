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
      <h1 style="text-indent: 1.5rem;" class="px-3 ">{{ testData.test_name }}</h1>
      <h3 style="text-indent: 1.5rem;" class="px-3">{{ testData.extra_data }}</h3>
      <div style="text-indent: 1.5rem; text-align: justify" v-html="testData.introduction" class="mt-3 px-3"></div>
    </div>
    <div v-if="this.questionList.length > 0">
      <form @submit="submitForm" method="POST">
        <input type="hidden" name="test_id" :value="testData.id">
        <div v-for="question in sortedQuestions" :key="question.id">
          <QuestionItemRunning :question="question" />
        </div>
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
      resultData: {}
    }
  },
  methods: {
    async submitForm(e) {
      this.isLoading = true
      e.preventDefault()

      try {
        const response = await axios.post(
          `${process.env.VUE_APP_BACKEND_PROTOCOL}://${process.env.VUE_APP_BACKEND_HOST}:${process.env.VUE_APP_BACKEND_PORT}/api/test-running/save/`,
          new FormData(e.target)
        )
        if (response.status == 200) {
          window.location.href = "http://localhost:8080/tests/running/1"
          // this.$router.replace({name: 'tests-running-success'})
        } else { throw new Error('POST data error')}

      } catch (error) {
        console.log(error.text)
      } finally {
        this.isLoading = false
      }
    }
  },
  computed: {
    sortedQuestions: function() {
      return this.questionList.sort(function(a, b) {
        if (a.index_number < b.index_number) {
          return -1
        }
        if (a.index_number > b.index_number) {
          return 1
        }
        return 0
      })
    }
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
  }
}
</script>

<style scoped></style>
