<template>
  <div class="form-check d-flex justify-content-between my-3">
    <div v-if="questionType === 1" class="d-flex align-items-center">
      <input class="form-check-input" type="radio" />
      <input
        type="text"
        class="form-control ms-2"
        v-model="answer.answer_text"
      />
    </div>
    <div v-if="questionType === 2" class="d-flex align-items-center">
      <input class="form-check-input" type="checkbox" />
      <input
        type="text"
        class="form-control ms-2"
        v-model="answer.answer_text"
      />
    </div>

    <div v-if="questionType === 3" class="d-flex align-items-center">
      <input type="text" class="form-control ms-2" disabled />
    </div>

    <div v-if="questionType === 4" class="d-flex align-items-center">
      {{ answer.index_number }}.
      <input
        type="text"
        class="form-control ms-2"
        v-model="answer.answer_text"
      />
    </div>

    <div v-if="questionType === 5" class="d-flex align-items-center">
      <input type="date" class="form-control ms-2" disabled />
    </div>

    <div class="d-flex align-items-center">
      <button
        type="button"
        class="btn-close"
        aria-label="Close"
        title="Удалить"
      ></button>
    </div>
  </div>
</template>

<script>
export default {
  name: "AnswerItem",
  props: {
    answer: Object,
    questionType: Number,
  },
}
</script>

<style scoped></style>
