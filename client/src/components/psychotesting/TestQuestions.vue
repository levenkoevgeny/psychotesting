<template>
  <div v-if="isError" class="alert alert-danger m-0 p-3" role="alert">
    Что-то пошло не так!
  </div>
  <div
    v-if="isLoading"
    class="d-flex justify-content-center align-items-center"
  >
    <Spinner />
  </div>
  <div v-else class="container">
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
          @click="() => addNewQuestion(0)"
        >
          <font-awesome-icon icon="fa-solid fa-circle-plus" />
        </button>
      </div>
      <div class="my-3">
        <input
          type="text"
          class="form-control fs-2"
          placeholder="Название теста"
          :class="{
            'border-danger': v$.testData.test_name.$silentErrors.length,
          }"
          v-model="testData.test_name"
          debounce="500"
        />

        <div
          :class="{
            invalid: v$.testData.test_name.$silentErrors.length,
            'visually-hidden': !v$.testData.test_name.$silentErrors.length,
          }"
        >
          Это поле не может быть пустым!
        </div>
      </div>
      <div class="mb-3">
        <textarea
          v-model="testData.extra_data"
          class="form-control fs-6"
          placeholder="Описание теста"
          rows="1"
        >{{ testData.extra_data }}
        </textarea>
      </div>
      <div class="mb-3">
        <textarea
          v-model="testData.introduction"
          class="form-control fs-6"
          placeholder="Вступительный текст"
          rows="5"
        >{{ testData.introduction }}
        </textarea>
      </div>
    </div>
    <div>
      <div v-if="questionList.length > 0">
        <div v-for="question in sortedQuestions" :key="question.id">
          <QuestionItem
            :question="question"
            @deleteQuestion="deleteQuestionHandler"
            @addNextQuestion="addNewQuestion"
            @copyQuestion="makeQuestionCopy"
            @setIsLoading="setIsLoading"
            @setIsError="setIsError"
            @sendSuccessToast="sendSuccessToast"
            @sendWarningToast="sendWarningToast"
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
import useVuelidate from "@vuelidate/core"
import { required } from "@vuelidate/validators"
import { useToast } from "vue-toastification"
import { toastOptions } from "@/utils"
import debounce from "lodash.debounce"

export default {
  name: "TestQuestions",
  components: { Spinner, QuestionItem },
  data() {
    return {
      testData: {
        test_name: null
      },
      questionList: [],
      isLoading: true,
      isError: false
    }
  },
  setup() {
    const toast = useToast()
    return { v$: useVuelidate(), toast }
  },
  validations() {
    return {
      testData: {
        test_name: { required }
      }
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
        this.questionList = await response.data
      }
    } catch (e) {
      this.isError = true
    } finally {
      this.isLoading = false
    }
  },
  methods: {
    arrangeIndexAdd(after) {
      this.questionList.map((question) => {
        if (parseInt(question.index_number) > parseInt(after)) {
          question.index_number = question.index_number + 1
        }
      })
    },
    arrangeIndexDelete(after) {
      this.questionList.map((question) => {
        if (parseInt(question.index_number) > parseInt(after)) {
          question.index_number = question.index_number - 1
        }
      })
    },
    setIsLoading(value) {
      this.isLoading = value
    },
    setIsError(value) {
      this.isError = value
    },
    sendSuccessToast() {
      this.toast.success("Сохранено!", {
        timeout: 700,
        closeOnClick: true
      })
    },
    sendWarningToast(warningText) {
      this.toast.warning(warningText, toastOptions)
    },
    async addNewQuestion(afterNumber) {
      try {
        const response = await questionsAPI.addNewQuestion(
          this.userToken,
          {
            test: this.testData.id,
            question_text: "Новый вопрос",
            question_type: 1,
            index_number: 1,
            is_active: true,
            has_required_answer: false,
            is_common_for_all_tests: false
          },
          afterNumber
        )
        this.arrangeIndexAdd(afterNumber)
        this.questionList.push(response.data)
      } catch (e) {
        this.isError = true
      }
    },
    async makeQuestionCopy(questionId, afterNumber) {
      try {
        const response = await questionsAPI.makeQuestionCopy(
          this.userToken,
          questionId
        )
        this.arrangeIndexAdd(afterNumber)
        this.questionList.push(response.data)
      } catch (error) {
        this.isError = true
      }
    },
    updateTestData: debounce(async function() {
      this.isError = false
      if (!this.v$.$invalid) {
        try {
          const response = await testDataAPI.updateTestData(
            this.userToken,
            this.testData
          )
          this.sendSuccessToast()
        } catch (error) {
          this.isError = true
        }
      }

    }, 500),
    async deleteQuestionHandler(questionId, afterNumber) {
      try {
        const response = await questionsAPI.deleteQuestion(
          this.userToken,
          questionId
        )
        this.questionList = this.questionList.filter(
          (question) => question.id !== questionId
        )
        this.arrangeIndexDelete(afterNumber)
        this.sendWarningToast("Вопрос удален!")
      } catch (error) {
        this.isError = true
      } finally {
      }
    }
  },
  watch: {
    testData: {
      handler(newValue, oldValue) {
        if (oldValue["test_name"] != null) {
          this.updateTestData()
        }
      },
      deep: true
    }
  }
}
</script>

<style scoped>
.invalid {
  color: #dc3545;
}

.display-visible {
  display: none;
}

.display-visible {
  display: block;
}
</style>
