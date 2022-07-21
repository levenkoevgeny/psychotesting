<template>
  <div class="container">
    <div style="background-color: white;height: 150px;"
         class="p-3 my-3 rounded-3 d-flex justify-content-center align-items-center flex-column component-white-background test-data-top-border">
      <h1>Спасибо за анкетирование!</h1>
<!--      <a href="/" class="link-secondary"><h3>Вернуться на главную</h3></a>-->
    </div>
  </div>
</template>

<script>
export default {
  name: "Success",
  data() {

  },
  created() {
    // this.timerId = setTimeout(() => this.$router.push({ name: 'main'}), 5000)
  },
  beforeUnmount() {
    // clearTimeout(this.timerId)
  }

}
</script>

<style scoped>

</style>