<template>
  <form @submit="submitHandler">
    <div class="mb-3">
      <label class="form-label">Login</label>
      <input type="text" class="form-control" v-model="auth_data.username" />
    </div>
    <div class="mb-3">
      <label class="form-label">Password</label>
      <input
        type="password"
        class="form-control"
        v-model="auth_data.password"
      />
    </div>
    <button type="submit" class="btn btn-primary">Submit</button>
  </form>
</template>

<script>
export default {
  name: "LoginView",
  data() {
    return {
      auth_data: {
        username: "",
        password: "",
      },
    }
  },
  methods: {
    submitHandler(e) {
      e.preventDefault()
      e.stopPropagation()
      console.log(this.auth_data)
      this.$store.dispatch("auth/actionLogIn", { ...this.auth_data })
    },
  },
}
</script>

<style scoped></style>
