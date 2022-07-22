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
      <table class="table table-bordered">
        <thead>
        <tr>
          <th scope="col" :colspan="question.answers.length" v-for="question in sortedQuestions" :key="question.id">
            {{ question.question_text }}
          </th>
        </tr>
        <tr>
          <template v-for="question in sortedQuestions" :key="question.id">
            <th v-for="answer in question.answers" :key="answer.id"
                v-if="[questionTypes['RADIO'], questionTypes['CHECKBOX'], questionTypes['SELECT']].includes(question.question_type)">
              {{ answer.answer_text }}
            </th>
            <th v-else></th>
          </template>
        </tr>
        </thead>
        <tbody>
        <tr>
          <template v-for="question in sortedQuestions" :key="question.id">
            <td v-for="answer in question.answers" :key="answer.id"
                v-if="[questionTypes['RADIO'], questionTypes['CHECKBOX'], questionTypes['SELECT']].includes(question.question_type)">{{resultsDict[answer.id]}}</td>
            <td v-else></td>
          </template>

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
import questionTypes from "@/components/psychotesting/questionTypes"

export default {
  name: "TestResultsAnswersCount",
  components: { Spinner },
  data() {
    return {
      testData: null,
      questionList: [],
      resultsDict: [],
      questionTypes: questionTypes,
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
      const testDataResultsResponse = await testDataAPI.getTestDataResultAnswersCount(
        this.userToken,
        this.$route.params.id
      )
      this.resultsDict = testDataResultsResponse.data
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