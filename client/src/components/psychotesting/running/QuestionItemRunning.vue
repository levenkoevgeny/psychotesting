<template>
  <div class="my-3 p-3 rounded-3 component-white-background component-left-border">
    <h5>{{ question.question_text }}</h5>
    <div v-for="(answer, index) in question.answers" :key="answer.id"
         v-if="question.question_type === questionTypes['RADIO'] ||
         question.question_type === questionTypes['CHECKBOX']">
      <AnswerItemRunning
        :answer="answer"
        :question="question"
        :index="index"
      />
    </div>

    <div v-if="question.question_type === questionTypes['SELECT']">
      <select class="form-select" :name="'question_' + question.id + '_select'">
        <option selected>--------</option>
        <option v-for="(answer) in question.answers" :key="answer.id" :value="answer.id">{{ answer.answer_text }}</option>
      </select>

    </div>

    <div v-if="question.question_type === questionTypes['TEXT']">
      <input
        type="text" class="form-control"
             :name="'question_' + question.id + '_text'" :required="question.has_required_answer">
    </div>

    <div v-if="question.question_type === questionTypes['DATE']">
      <input
        type="date" class="form-control"
        :name="'question_' + question.id + '_date'" :required="question.has_required_answer">
    </div>


  </div>
</template>

<script>
import AnswerItemRunning from "@/components/psychotesting/running/AnswerItemRunning"
import Spinner from "@/components/common/Spinner"
import questionTypes from "@/components/psychotesting/questionTypes"

export default {
  name: "QuestionItemRunning",
  components: { Spinner, AnswerItemRunning },
  props: {
    question: { type: Object, required: true }
  },
  data() {
    return {
      questionTypes: questionTypes,
      isLoading: false,
      isError: false
    }
  }
}
</script>

<style scoped>

</style>