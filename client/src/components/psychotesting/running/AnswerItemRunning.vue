<template>

  <div v-if="question.question_type === questionTypes['RADIO']" class="form-check my-2">
    <input
      class="form-check-input"
      type="radio"
      :name="'question_' + question.id + '_radio'"
      :value="answer.id"
      :required="question.has_required_answer"
      @change="changeHandler"
    />
    <label class="form-check-label">
      {{ answer.answer_text }}
    </label>
    <div style="display: none">
      <input type="text" class="form-control" disabled>
    </div>
  </div>

  <div v-if="question.question_type === questionTypes['CHECKBOX']" class="form-check my-2">
    <input
      class="form-check-input"
      type="checkbox"
      :name="'question_' + question.id + '_checkbox_' + index"
      :value="answer.id"
      :required="question.has_required_answer"
      @change="changeHandler"
    />
    <label class="form-check-label" for="flexRadioDefault1">
      {{ answer.answer_text }}
    </label>
    <div style="display: none">
      <input type="text" class="form-control" disabled>
    </div>
  </div>


</template>

<script>
import questionTypes from "@/components/psychotesting/questionTypes"

export default {
  name: "AnswerItemRunning",
  props: {
    answer: { type: Object, required: true },
    question: { type: Object, required: true },
    index: { type: Number, required: true },
  },
  data() {
    return {
      questionTypes: questionTypes,
      radioStatus: false
    }
  },
  methods: {
    changeHandler(e) {
      if (e.target.checked) {
        console.log(e.target.checked)
      } else {
        console.log(e.target.checked)
      }

    }
  },
  computed: {

  }
}
</script>

<style scoped>

</style>