<template>
  <div
    class="my-3 p-3 rounded-3 component-white-background component-left-border"
  >
    <h3
      class="p-3"
      style="border-bottom: 5px solid grey; background-color: lightblue"
    >
      {{ question.question_text }}
    </h3>

    <div
      v-for="(answer, index) in question.answers"
      :key="answer.id"
      class="form-check my-3"
    >
      <input
        class="form-check-input"
        type="radio"
        name="flexRadioDefault"
        id="flexRadioDefault1"
      />
      <label class="form-check-label" for="flexRadioDefault1">
        {{ answer.answer_text }}
      </label>
    </div>
  </div>
</template>

<script>
export default {
  name: "QuestionItem",
  props: {
    question: Object,
  },
}
</script>

<style scoped></style>
