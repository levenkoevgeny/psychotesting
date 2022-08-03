<template>
  <div
    v-if="question.question_type === questionTypes['RADIO']"
    class="form-check my-2"
  >
    <input
      class="form-check-input"
      type="radio"
      :name="'question_' + question.id + '_radio'"
      :value="answer.id"
      :required="question.has_required_answer"
      @change="$emit('changeRadioValue', answer.id)"
    />
    <label class="form-check-label">
      {{ answer.answer_text }}
    </label>
    <div v-if="answer.id === radioValue && answer.has_extra_data">
      <input
        type="text"
        class="form-control"
        :name="'question_' + question.id + '_radio_extra_input'"
        required
      />
    </div>
  </div>

  <div
    v-if="question.question_type === questionTypes['CHECKBOX']"
    class="form-check my-2"
  >
    <input
      class="form-check-input"
      type="checkbox"
      :name="'question_' + question.id + '_checkbox_' + index"
      :value="answer.id"
      @change="checkboxChangeHandler"
    />
    <label class="form-check-label">
      {{ answer.answer_text }}
    </label>
    <div
      v-bind:class="{ checkbox_display_none: checkBoxStatus }"
      v-if="answer.has_extra_data"
    >
      <input
        type="text"
        class="form-control my-2"
        :disabled="checkBoxStatus"
        :name="
          'question_' + question.id + '_checkbox_' + index + '_extra_input'
        "
        :required="!checkBoxStatus"
      />
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
    radioValue: { type: Number, required: true },
  },
  data() {
    return {
      questionTypes: questionTypes,
      radioStatus: false,
      checkBoxStatus: true,
    }
  },
  methods: {
    checkboxChangeHandler(e) {
      if (e.target.checked) {
        this.checkBoxStatus = false
      } else {
        this.checkBoxStatus = true
      }
    },
  },
  computed: {},
}
</script>

<style scoped>
.checkbox_display_none {
  display: none;
}
</style>
