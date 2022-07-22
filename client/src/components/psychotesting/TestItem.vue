<template>
  <div
    class="my-3 p-3 rounded-3 component-white-background component-left-border"
  >
    <router-link :to="{ name: 'test_questions', params: { id: testData.id } }" class="fs-5 fw-bold">
      {{ testData.test_name }}
    </router-link>
    <p class="card-text">{{ testData.extra_data }}</p>
    <small>Количество вопросов - {{ testData.get_questions_count }}</small><br />
    <small
    >Дата создания -
      {{ addedTimeToLocalString(testData.data_created) }}</small
    >
    <hr class="dropdown-divider my-3" />
    <div class="row">
      <div
        class="col-md-6 col-lg-8 border-end d-flex justify-content-md-end my-1"
      >
        <button
          type="button"
          class="btn btn-light rounded-circle link-secondary mx-2 fs-5"
          title="Просмотр"
          @click="changeRoute(testData.id)"
        >
          <font-awesome-icon icon="fa-solid fa-eye" />
        </button>
        <a class="nav-link link-secondary dropdown-toggle mx-2 fs-5" data-bs-toggle="dropdown" href="#" role="button"
           aria-expanded="false">
          <font-awesome-icon icon="fa-solid fa-square-poll-vertical" />
        </a>
        <ul class="dropdown-menu">
          <li>
            <router-link :to="{ name: 'test_result_full_text', params: { id: testData.id } }" class="dropdown-item">
              Полный текст
            </router-link>
          </li>
          <li>
            <router-link :to="{ name: 'test_result_answers_count', params: { id: testData.id } }" class="dropdown-item">
              Количество ответов
            </router-link>
          </li>
          <li>
            <router-link :to="{ name: 'test_result_answers_1_0', params: { id: testData.id } }" class="dropdown-item">
              Ответы "1" "0"
            </router-link>
          </li>

        </ul>
        <button
          type="button"
          class="btn btn-light rounded-circle link-secondary mx-2 fs-5"
          title="Создать копию"
          @click="$emit('makeTestCopy', testData.id)"
        >
          <font-awesome-icon icon="fa-regular fa-clone" />
        </button>
        <button
          type="button"
          class="btn btn-light rounded-circle link-secondary mx-2 fs-5"
          title="Удалить"
          @click="$emit('deleteTest', testData.id)"
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
            v-model="testData.is_active"
          />
          <label class="form-check-label">Активный</label>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { testDataAPI } from "@/api/testDataApi"
import { mapGetters } from "vuex"

export default {
  name: "TestItem",
  props: {
    testData: { type: Object, required: true }
  },
  methods: {
    addedTimeToLocalString(testDateTime) {
      const IsoDate = new Date(testDateTime)
      return IsoDate.toLocaleDateString() + " " + IsoDate.toLocaleTimeString()
    },
    async updateTestData() {
      await testDataAPI.updateTestData(this.userToken, this.testData)
    },
    changeRoute(testId) {
      let route = this.$router.resolve({
        name: "test_running",
        params: { id: testId }
      })
      window.open(route.href, "_blank")
    }
  },
  computed: {
    ...mapGetters({
      userData: "auth/getUser",
      userToken: "auth/getToken"
    })
  },
  watch: {
    testData: {
      handler(newValue, oldValue) {
        this.updateTestData()
      },
      deep: true
    }
  }
}
</script>

<style scoped></style>
