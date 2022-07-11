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
    <div v-for="(answer, index) in question.answers" :key="answer.id">
      <AnswerItem
        :answer="answer"
        :questionType="parseInt(question.question_type)"
      />
    </div>

    <!--    add new answer-->

    <div
      class="d-flex align-items-center flex-row my-3"
      v-if="parseInt(question.question_type) === 1"
    >
      <div class="d-flex align-items-center">
        <input class="form-check-input" type="radio" />
        <input type="text" class="form-control ms-2" value="Добавить вариант" />
      </div>
      <div class="d-flex align-items-center flex-row">
        <span class="ms-2">или</span>
        <button
          type="button"
          class="btn btn-link ms-2 px-0"
          style="text-decoration: none"
        >
          Добавить вариант "Другое"
        </button>
      </div>
    </div>
    <div
      class="d-flex align-items-center flex-row my-3"
      v-if="parseInt(question.question_type) === 2"
    >
      <div class="d-flex align-items-center">
        <input class="form-check-input" type="checkbox" />
        <input type="text" class="form-control ms-2" value="Добавить вариант" />
      </div>
      <div class="d-flex align-items-center flex-row">
        <span class="ms-2">или</span>
        <button
          type="button"
          class="btn btn-link ms-2 px-0"
          style="text-decoration: none"
        >
          Добавить вариант "Другое"
        </button>
      </div>
    </div>
    <div
      class="d-flex align-items-center flex-row my-3"
      v-if="parseInt(question.question_type) === 4"
    >
      <div class="d-flex align-items-center">
        <input type="text" class="form-control ms-2" value="Добавить вариант" />
      </div>
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
        >
          <font-awesome-icon icon="fa-regular fa-clone" />
        </button>
        <button
          type="button"
          class="btn btn-light rounded-circle link-secondary mx-2 fs-5"
          title="Удалить"
          @click="$emit('deleteQuestion', question.id)"
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
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from "vuex"
import AnswerItem from "@/components/psychotesting/AnswerItem"
import { questionsAPI } from "@/api/questionsAPI"
export default {
  name: "QuestionItem",
  components: { AnswerItem },
  props: {
    question: Object,
  },
  methods: {
    async updateQuestionData() {
      await questionsAPI.updateQuestion(this.userToken, this.question)
    },
  },
  computed: {
    ...mapGetters({
      userToken: "auth/getToken",
    }),
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
