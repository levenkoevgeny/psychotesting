<template></template>

<script>
import Spinner from "@/components/common/Spinner"
import { testDataAPI } from "@/api/testDataApi"
import { questionsAPI } from "@/api/questionsAPI"

export default {
  name: "TestRunning",
  components: { Spinner },
  data() {
    return {
      testData: null,
      questionList: [],
      isQuestionListLoading: true,
      isTestDataLoading: true,
    }
  },
  methods: {},
  computed: {},
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
        this.isQuestionListLoading = false
      }
    } catch (e) {
    } finally {
      this.isTestDataLoading = false
    }
  },
}
</script>

<style scoped></style>
