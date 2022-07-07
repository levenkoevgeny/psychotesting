<template>
  <div
    class="container mt-3 p-3 rounded-3 component-white-background test-data-top-border"
  >
    <h6 v-if="isSaving" class="d-inline-block mt-3">Сохранение...</h6>
    <h6 v-else class="d-inline-block mt-3">
      Сохранено
      <font-awesome-icon icon="fa-regular fa-circle-check" />
    </h6>
    <h1>Редактирование персональных данных</h1>
    <a href="/">Вернуться на главную</a>

    <div class="my-3">
      <label class="form-label">Название организации</label>
      <input type="email" class="form-control" />
    </div>
  </div>
</template>

<script>
import { mapGetters } from "vuex"

export default {
  name: "OrganisationData",
  data() {
    return {
      isSaving: false,
    }
  },
  computed: {
    ...mapGetters({
      userToken: "auth/getToken",
      userData: "auth/getUser",
    }),
  },
}
</script>

<style scoped></style>
