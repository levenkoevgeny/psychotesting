<template>
  <div
    class="my-3 p-3 rounded-3 component-white-background test-data-top-border"
  >
    <h1 v-if="testData">{{ testData.test_name }}</h1>
    <h5 v-if="testData">{{ testData.extra_data }}</h5>
  </div>

  <div v-if="isQuestionListLoading"><Spinner /></div>
  <div v-else>
    <div v-if="questionList.length > 0">
      <p v-for="(question, index) in questionList" :key="question.id">
        <QuestionItem :question="question" />
      </p>
    </div>
    <div v-else>Список пуст</div>
  </div>
</template>

<script>
import Spinner from "@/components/common/Spinner"
import QuestionItem from "@/components/psychotesting/QuestionItem"
export default {
  name: "TestQuestions",
  components: { Spinner, QuestionItem },
  data() {
    return {
      testData: null,
      questionList: [],
      isQuestionListLoading: true,
      isTestDataLoading: true,
    }
  },
  created() {
    fetch(
      `${process.env.VUE_APP_BACKEND_PROTOCOL}://${process.env.VUE_APP_BACKEND_HOST}:${process.env.VUE_APP_BACKEND_PORT}/api/test-data/${this.$route.params.id}`
    )
      .then((response) => response.json())
      .then((test) => {
        this.testData = test
      })
      .catch((e) => alert(e))
      .finally(() => (this.isTestDataLoading = false))
    fetch(
      `${process.env.VUE_APP_BACKEND_PROTOCOL}://${process.env.VUE_APP_BACKEND_HOST}:${process.env.VUE_APP_BACKEND_PORT}/api/questions/?test_id=${this.$route.params.id}`
    )
      .then((response) => response.json())
      .then((questions) => {
        this.questionList = questions
      })
      .catch((e) => alert(e))
      .finally(() => (this.isQuestionListLoading = false))
  },
}
</script>

<style scoped></style>
