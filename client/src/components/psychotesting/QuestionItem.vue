<template>
  <div
    class="my-3 p-3 rounded-3 component-white-background component-left-border"
  >
    <div class="row">
      <div class="col-md-6">
        <div class="my-3">
          <input
            v-model="question.question_text"
            type="text"
            class="form-control"
            placeholder="Текст вопроса"
          />
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
    <div
      class="p-3"
      v-if="parseInt(question.question_type) === questionTypes['RADIO']"
    >
      <div>
        <div v-for="answer in sortedAnswers" :key="answer.id">
          <AnswerItem
            :answer="answer"
            :questionType="parseInt(question.question_type)"
            :moreThanOneAnswer="answersCount"
            :questionTypes="questionTypes"
            @deleteAnswer="deleteAnswer"
          />
        </div>
      </div>
      <div class="d-flex align-items-center">
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
    <div
      class="p-3"
      v-if="parseInt(question.question_type) === questionTypes['CHECKBOX']"
    >
      <div>
        <div v-for="answer in sortedAnswers" :key="answer.id">
          <AnswerItem
            :answer="answer"
            :questionType="parseInt(question.question_type)"
            :moreThanOneAnswer="answersCount"
            :questionTypes="questionTypes"
            @deleteAnswer="deleteAnswer"
          />
        </div>
      </div>
      <div class="d-flex align-items-center">
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
    <div
      class="p-3"
      v-if="parseInt(question.question_type) === questionTypes['SELECT']"
    >
      <div>
        <div v-for="answer in sortedAnswers" :key="answer.id">
          <AnswerItem
            :answer="answer"
            :questionType="parseInt(question.question_type)"
            :moreThanOneAnswer="answersCount"
            :questionTypes="questionTypes"
            @deleteAnswer="deleteAnswer"
          />
        </div>
      </div>
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
      class="p-3"
      v-if="parseInt(question.question_type) === questionTypes['TEXT']"
    >
      <input type="text" class="form-control" disabled style="width: 50%" />
    </div>

    <!--    date-->
    <div
      class="p-3"
      v-if="parseInt(question.question_type) === questionTypes['DATE']"
    >
      <input type="date" class="form-control" disabled style="width: 50%" />
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
          @click="$emit('deleteQuestion', question.id, question.index_number)"
        >
          <font-awesome-icon icon="fa-regular fa-trash-can" />
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
        <button
          type="button"
          class="btn btn-light rounded-circle link-secondary mx-2 fs-5"
          title="Добавить новый вопрос"
          @click="$emit('addNextQuestion', question.index_number)"
        >
          <font-awesome-icon icon="fa-solid fa-plus" />
        </button>
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
    updateQuestionData: debounce(async function() {
      this.$emit("setSaving", true)
      if (
        [this.questionTypes["TEXT"], this.questionTypes["DATE"]].includes(
          parseInt(this.question.question_type)
        )
      ) {
        // const response = await questionsAPI.deleteQuestionAnswers(
        //   this.userToken,
        //   this.question.id
        // )
        // console.log("sdfsdf")
        // this.$emit("updateQuestions", response.data)
      }
      await questionsAPI.updateQuestion(this.userToken, this.question)
      this.$emit("setSaving", false)
    }, 500),
    async deleteAnswer(answerId, after) {
      try {
        await answerAPI.deleteAnswer(this.userToken, answerId)
        this.question.answers = this.question.answers.filter(
          (answer) => answer.id !== answerId
        )
        this.isSaving = false
        this.arrangeIndexDelete(after)
      } catch (e) {
      } finally {
      }
    },
    async addAnswer() {
      try {
        const response = await answerAPI.addNewAnswer(this.userToken, {
          question: this.question.id,
          answer_text: "Новый ответ",
        })
        this.question.answers.push(response.data)
      } catch (error) {
      } finally {
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
  },

  watch: {
    question: {
      handler(newValue, oldValue) {
        this.updateQuestionData()
      },
      deep: true,
    },
  },
}
</script>

<style scoped></style>
