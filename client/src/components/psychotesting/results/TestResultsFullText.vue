<template>
  <div v-if="isError" class="alert alert-danger m-0 p-3" role="alert">
    Ошибка загрузки данных!
  </div>
  <div
    v-if="isLoading"
    class="d-flex justify-content-center align-items-center"
    style="height: 80vh"
  >
    <Spinner />
  </div>
  <div v-else class="container-fluid">
    <div v-if="questionList.length > 0">
      <table class="table">
        <thead>
        <tr>
          <th>Дата</th>
          <th scope="col" v-for="question in sortedQuestions" :key="question.id">{{ question.question_text }}</th>
        </tr>
        </thead>
        <tbody>
        <tr v-for="result in resultsList" :key="result.id">
          <td><nobr>{{result['date']}}</nobr></td>
          <td v-for="question in sortedQuestions" :key="question.id">{{result[question.id]}}</td>
        </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import { mapGetters } from "vuex"
import { testDataAPI } from "@/api/testDataApi"
import { questionsAPI } from "@/api/questionsAPI"
import Spinner from "@/components/common/Spinner"

export default {
  name: "TestResults",
  components: { Spinner },
  data() {
    return {
      testData: null,
      questionList: [],
      resultsList: [],
      isLoading: true,
      isError: false
    }
  },
  computed: {
    ...mapGetters({
      userToken: "auth/getToken"
    }),
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
      const questionsResponse = await questionsAPI.getQuestionsByTest(
        this.userToken,
        this.$route.params.id
      )
      this.questionList = await questionsResponse.data
      const testDataResultsResponse = await testDataAPI.getTestDataResultFullText(
        this.userToken,
        this.$route.params.id
      )
      this.resultsList = testDataResultsResponse.data
    } catch (error) {
      this.isError = true
    } finally {
      this.isLoading = false
    }
  }
}
</script>

<style scoped>

</style>