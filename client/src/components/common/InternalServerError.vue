<template>
  <div
    class="container mt-3 p-3 rounded-3 component-white-background test-data-top-border"
  >
    <h1>Внутренняя ошибка сервера</h1>
  </div>
</template>

<script>
import router from "@/router/router"
export default {
  name: "InternalServerError",
  data() {
    return {
      timerId: null,
    }
  },
  created() {
    this.timerId = setInterval(() => router.push({ name: "main" }), 5000)
  },
  unmounted() {
    clearInterval(this.timerId)
  },
}
</script>

<style scoped></style>
