<template>
  <div
    class="my-3 p-3 rounded-3 component-white-background component-left-border"
  >
    <router-link :to="{ name: 'test_questions', params: { id: testData.id } }">
      <h5>{{ testData.test_name }}</h5>
    </router-link>
    <p class="card-text">{{ testData.extra_data }}</p>
    <small>Количество вопросов - {{ testData.get_questions_count }}</small
    ><br />
    <small
      >Дата создания -
      {{ this.addedTimeToLocalString(testData.data_created) }}</small
    >
    <hr class="dropdown-divider my-3" />
    <div class="row">
      <div
        class="col-md-6 col-lg-8 border-end d-flex justify-content-md-end my-1"
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
    testData: Object,
  },
  methods: {
    addedTimeToLocalString(testDateTime) {
      const IsoDate = new Date(testDateTime)
      return IsoDate.toLocaleDateString() + " " + IsoDate.toLocaleTimeString()
    },
    async updateTestData() {
      await testDataAPI.updateTestData(this.userToken, this.testData)
    },
  },
  computed: {
    ...mapGetters({
      userData: "auth/getUser",
      userToken: "auth/getToken",
    }),
  },
  watch: {
    testData: {
      handler(newValue, oldValue) {
        this.updateTestData()
      },
      deep: true,
    },
  },
}
</script>

<style scoped></style>
