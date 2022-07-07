<template>
  <div
    class="d-flex justify-content-center align-items-center container-fluid"
    style="background-color: #f5f5f5; height: 100vh"
  >
    <main class="form-signin">
      <form @submit="submitHandler">
        <h1 class="h3 mb-3 fw-normal">Авторизуйтесь</h1>

        <div class="form-floating">
          <input
            type="text"
            class="form-control"
            placeholder="name@example.com"
            v-model="auth_data.username"
          />
          <label>Логин</label>
        </div>
        <div class="form-floating">
          <input
            type="password"
            class="form-control"
            placeholder="Password"
            v-model="auth_data.password"
          />
          <label>Пароль</label>
        </div>
        <button class="w-100 btn btn-lg btn-primary" type="submit">Вход</button>
        <br />
        <br />
        <a class="" href="/registration">Нет аккаунта?</a>
        <p class="mt-5 mb-3 text-muted">&copy; Разработано ООИТ Академии МВД</p>
      </form>
    </main>
  </div>
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
      // this.$store.commit("auth/setIsLogInError", false)
      this.$store
        .dispatch("auth/actionLogIn", { ...this.auth_data })
        .then(() => {
          this.$router.replace(this.$route.query.redirect || "/")
        })
    },
  },
}
</script>

<style scoped>
.bd-placeholder-img {
  font-size: 1.125rem;
  text-anchor: middle;
  -webkit-user-select: none;
  -moz-user-select: none;
  user-select: none;
}

@media (min-width: 768px) {
  .bd-placeholder-img-lg {
    font-size: 3.5rem;
  }
}

body-signin {
  height: 100%;
  display: flex;
  align-items: center;
  padding-top: 40px;
  padding-bottom: 40px;
  background-color: #f5f5f5;
}

.form-signin {
  width: 100%;
  max-width: 330px;
  padding: 15px;
  margin: auto;
}

.form-signin .checkbox {
  font-weight: 400;
}

.form-signin .form-floating:focus-within {
  z-index: 2;
}

.form-signin input[type="text"] {
  margin-bottom: -1px;
  border-bottom-right-radius: 0;
  border-bottom-left-radius: 0;
}

.form-signin input[type="password"] {
  margin-bottom: 10px;
  border-top-left-radius: 0;
  border-top-right-radius: 0;
}
</style>
