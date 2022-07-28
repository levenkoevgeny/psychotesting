<template>
  <div
    class="my-3 p-2 rounded-3 component-white-background component-left-border"
  >
    <div class="row py-2 px-3">
      <div class="col-md-6">
        <div class="my-3">
          <input
            v-model="question.question_text"
            type="text"
            class="form-control"
            placeholder="Текст вопроса"
          />
          <div
            :class="{
              invalid: v$.question.question_text.$silentErrors.length,
              'visually-hidden':
                !v$.question.question_text.$silentErrors.length,
            }"
          >
            Это поле не может быть пустым!
          </div>
        </div>
      </div>
      <div class="col-md-6">
        <div class="my-3">
          <select
            class="form-select"
            aria-label="Default select example"
            v-model="question.question_type"
          >
            <option value="1" data-icon="glyphicon glyphicon-eye-open">
              Один из списка
            </option>
            <option value="2">Несколько из списка</option>
            <option value="3">Текст</option>
            <option value="4">Раскрывающийся список</option>
            <option value="5">Дата</option>
          </select>
        </div>
      </div>
    </div>

    <!--    radio-->
    <div v-if="parseInt(question.question_type) === questionTypes['RADIO']">
      <AnswerItem
        v-for="answer in sortedAnswers"
        :key="answer.id"
        :answer="answer"
        :questionType="parseInt(question.question_type)"
        :moreThanOneAnswer="answersCount"
        :questionTypes="questionTypes"
        @deleteAnswer="deleteAnswer"
      />

      <div class="d-flex align-items-center my-2 py-2 px-3">
        <input class="form-check-input" type="radio" />
        <button
          type="button"
          class="btn btn-link"
          style="text-decoration: none"
          @click="addAnswer"
        >
          Добавить вариант
        </button>
      </div>
    </div>
    <!--    checkbox-->
    <div v-if="parseInt(question.question_type) === questionTypes['CHECKBOX']">
      <AnswerItem
        v-for="answer in sortedAnswers"
        :key="answer.id"
        :answer="answer"
        :questionType="parseInt(question.question_type)"
        :moreThanOneAnswer="answersCount"
        :questionTypes="questionTypes"
        @deleteAnswer="deleteAnswer"
      />

      <div class="d-flex align-items-center my-2 py-2 px-3">
        <input class="form-check-input" type="checkbox" />
        <button
          type="button"
          class="btn btn-link"
          style="text-decoration: none"
          @click="addAnswer"
        >
          Добавить вариант
        </button>
      </div>
    </div>
    <!--    select-->
    <div v-if="parseInt(question.question_type) === questionTypes['SELECT']">
      <AnswerItem
        v-for="answer in sortedAnswers"
        :key="answer.id"
        :answer="answer"
        :questionType="parseInt(question.question_type)"
        :moreThanOneAnswer="answersCount"
        :questionTypes="questionTypes"
        @deleteAnswer="deleteAnswer"
      />

      <div class="d-flex align-items-center">
        <button
          type="button"
          class="btn btn-link ms-4"
          style="text-decoration: none"
          @click="addAnswer"
        >
          Добавить вариант
        </button>
      </div>
    </div>

    <!--    text-->
    <div
      class="px-3"
      v-if="parseInt(question.question_type) === questionTypes['TEXT']"
    >
      <input type="text" class="form-control mt-2" disabled />
    </div>

    <!--    date-->
    <div
      class="px-3"
      v-if="parseInt(question.question_type) === questionTypes['DATE']"
    >
      <input type="date" class="form-control" disabled />
    </div>

    <hr class="dropdown-divider my-3" />
    <div class="row">
      <div
        class="col-md-6 col-lg-8 border-end d-flex justify-content-md-end my-2"
      >
        <button
          type="button"
          class="btn btn-light rounded-circle link-secondary mx-2 fs-5"
          title="Создать копию"
          @click="$emit('copyQuestion', question.id, question.index_number)"
        >
          <font-awesome-icon icon="fa-regular fa-clone" />
        </button>
        <button
          type="button"
          class="btn btn-light rounded-circle link-secondary mx-2 fs-5"
          title="Удалить"
          @click="
            deleteQuestionHandler($event, question.id, question.index_number)
          "
        >
          <font-awesome-icon icon="fa-regular fa-trash-can" />
        </button>
        <button
          type="button"
          class="btn btn-light rounded-circle link-secondary mx-2 fs-5"
          title="Добавить новый вопрос"
          @click="$emit('addNextQuestion', question.index_number)"
        >
          <font-awesome-icon icon="fa-solid fa-plus" />
        </button>
      </div>
      <div class="col-md-6 col-lg-4 d-flex align-items-center">
        <div class="form-check form-switch ms-3 my-2">
          <input
            class="form-check-input"
            type="checkbox"
            role="switch"
            v-model="question.has_required_answer"
          />
          <label class="form-check-label">Обязательный вопрос</label>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from "vuex"
import AnswerItem from "@/components/psychotesting/AnswerItem"
import { questionsAPI } from "@/api/questionsAPI"
import { answerAPI } from "@/api/answerAPI"
import questionTypes from "@/components/psychotesting/questionTypes"

import debounce from "lodash.debounce"
import { useToast } from "vue-toastification"
import useVuelidate from "@vuelidate/core"
import { required } from "@vuelidate/validators"

export default {
  name: "QuestionItem",
  components: { AnswerItem },
  props: {
    question: { type: Object, required: true },
  },
  data() {
    return {
      questionTypes: questionTypes,
    }
  },
  setup() {
    const toast = useToast()
    return { v$: useVuelidate(), toast }
  },
  validations() {
    return {
      question: {
        question_text: { required },
      },
    }
  },
  methods: {
    arrangeIndexAdd(after) {
      this.question.answers.map((answer) => {
        if (parseInt(answer.index_number) > parseInt(after)) {
          answer.index_number = answer.index_number + 1
        }
      })
    },
    arrangeIndexDelete(after) {
      this.question.answers.map((answer) => {
        if (parseInt(answer.index_number) > parseInt(after)) {
          answer.index_number = answer.index_number - 1
        }
      })
    },
    updateQuestionData: debounce(async function () {
      try {
        this.$emit("setIsError", false)
        const response = await questionsAPI.updateQuestion(
          this.userToken,
          this.question
        )
        if (response.status >= 200 && response.status < 300) {
          this.$emit("sendSuccessToast")
        } else throw new Error()
      } catch (e) {
        this.$emit("setIsError", true)
      }
    }, 500),
    async deleteQuestionHandler(event, question_id, question_index_number) {
      event.target.disabled = true
      this.$emit("deleteQuestion", question_id, question_index_number)
    },
    async addAnswer() {
      try {
        const response = await answerAPI.addNewAnswer(this.userToken, {
          question: this.question.id,
          answer_text: "Новый ответ",
        })
        if (response.status >= 200 && response.status < 300) {
          this.question.answers.push(response.data)
        }
      } catch (error) {
        this.$emit("setIsError", true)
      }
    },
    async deleteAnswer(answerId, after) {
      try {
        const response = await answerAPI.deleteAnswer(this.userToken, answerId)
        if (response.status >= 200 && response.status < 300) {
          this.question.answers = this.question.answers.filter(
            (answer) => answer.id !== answerId
          )
          this.arrangeIndexDelete(after)
          this.$emit("sendWarningToast", "Ответ удален!")
        } else throw new Error("")
      } catch (e) {
        this.$emit("setIsError", true)
      }
    },
  },
  computed: {
    ...mapGetters({
      userToken: "auth/getToken",
    }),
    sortedAnswers: function () {
      return this.question.answers.sort(function (a, b) {
        if (a.index_number < b.index_number) {
          return -1
        }
        if (a.index_number > b.index_number) {
          return 1
        }
        return 0
      })
    },
    answersCount: function () {
      return this.question.answers.length > 1
    },
    get_question_text() {
      return this.question.question_text
    },
    get_question_type() {
      return this.question.question_type
    },
  },

  watch: {
    get_question_text: {
      handler(newValue, oldValue) {
        if (!this.v$.$invalid) {
          this.updateQuestionData()
        }
      },
    },
    get_question_type: {
      handler(newValue, oldValue) {
        this.updateQuestionData()
      },
    },
  },
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
