<template>
  <div class="row my-2 py-2 px-3">
    <div class="col-md-6">
      <div class="form-check">
        <div
          v-if="questionType === questionTypes['RADIO']"
          class="d-flex align-items-center"
        >
          <input class="form-check-input" type="radio" :value="answer.id" />
          <input
            type="text"
            class="form-control ms-2"
            v-model="answer.answer_text"
          />
        </div>
        <div
          v-if="questionType === questionTypes['CHECKBOX']"
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
          v-if="questionType === questionTypes['SELECT']"
          class="d-flex align-items-center"
        >
          <p
            style="
              margin-left: -1.5rem;
              width: 1em;
              height: 1em;
              margin-top: 0.5em;
              vertical-align: center;
            "
          >
            {{ answer.index_number }}.
          </p>
          <input
            type="text"
            class="form-control ms-2"
            v-model="answer.answer_text"
          />
        </div>
      </div>
    </div>
    <div
      class="col-md-6 d-flex flex-row align-items-center justify-content-between ps-3"
    >
      <!--additional info-->
      <div
        v-if="
          questionType === questionTypes['RADIO'] ||
          questionType === questionTypes['CHECKBOX']
        "
      >
        <div class="form-check form-switch ms-3 my-2">
          <input
            class="form-check-input"
            type="checkbox"
            role="switch"
            v-model="answer.has_extra_data"
          />
          <label class="form-check-label">Дополнительная информация</label>
        </div>
      </div>
      <div v-if="questionType === questionTypes['SELECT']"></div>
      <!--delete button-->
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
  </div>
</template>

<script>
import questionTypes from "@/components/psychotesting/questionTypes"
import { mapGetters } from "vuex"
import { answerAPI } from "@/api/answerAPI"

import debounce from "lodash.debounce"
import { useToast } from "vue-toastification"

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
  setup() {
    const toast = useToast()
    return { toast }
  },
  methods: {
    updateAnswerData: debounce(async function () {
      try {
        await answerAPI.updateAnswerData(this.userToken, this.answer)
      } catch (e) {
        this.$parent.$emit("setIsError", true)
      } finally {
        this.$parent.$emit("sendSuccessToast")
      }
    }, 500),
  },
  computed: {
    ...mapGetters({
      userToken: "auth/getToken",
    }),
  },
  watch: {
    answer: {
      handler(newValue, oldValue) {
        console.log("ans")
        this.updateAnswerData()
      },
      deep: true,
    },
  },
}
</script>

<style scoped></style>
