<template>
  <div class="form-check d-flex justify-content-between my-3">
    <div
      v-if="questionType === this.questionTypes['RADIO']"
      class="d-flex align-items-center"
    >
      <input class="form-check-input" type="radio" />
      <input
        type="text"
        class="form-control ms-2"
        v-model="answer.answer_text"
      />
    </div>
    <div
      v-if="questionType === this.questionTypes['CHECKBOX']"
      class="d-flex align-items-center"
    >
      <input class="form-check-input" type="checkbox" />
      <input
        type="text"
        class="form-control ms-2"
        v-model="answer.answer_text"
      />
    </div>

    <div
      v-if="questionType === this.questionTypes['TEXT']"
      class="d-flex align-items-center"
    >
      <input type="text" class="form-control ms-2" disabled />
    </div>

    <div
      v-if="questionType === this.questionTypes['SELECT']"
      class="d-flex align-items-center"
    >
      {{ answer.index_number }}.
      <input
        type="text"
        class="form-control ms-2"
        v-model="answer.answer_text"
      />
    </div>

    <div
      v-if="questionType === this.questionTypes['DATE']"
      class="d-flex align-items-center"
    >
      <input type="date" class="form-control ms-2" disabled />
    </div>

    <div class="d-flex align-items-center" v-if="moreThanOneAnswer">
      <button
        type="button"
        class="btn-close"
        aria-label="Close"
        title="Удалить"
        @click="$emit('deleteAnswer', answer.id, answer.index_number)"
      ></button>
    </div>
  </div>
</template>

<script>
import questionTypes from "@/components/psychotesting/questionTypes"
import { mapGetters } from "vuex"
import { answerAPI } from "@/api/answerAPI"

export default {
  name: "AnswerItem",
  props: {
    answer: { type: Object, required: true },
    questionType: { type: Number, required: true },
    moreThanOneAnswer: { type: Boolean, required: true },
  },
  data() {
    return {
      questionTypes: questionTypes,
    }
  },
  methods: {
    async updateAnswerData() {
      await answerAPI.updateAnswerData(this.userToken, this.answer)
    },
  },
  computed: {
    ...mapGetters({
      userToken: "auth/getToken",
    }),
  },
  watch: {
    answer: {
      handler(newValue, oldValue) {
        this.updateAnswerData()
      },
      deep: true,
    },
  },
}
</script>

<style scoped></style>
