<template>
  <div
    class="d-flex justify-content-center align-items-center container-fluid"
    style="background-color: #f5f5f5; height: 100vh"
  >

    <div class="fixed-top m-3"><a href="/login">Вход в систему</a></div>

    <main class="form-signin">
      <div class="alert alert-danger" v-if="v$.$errors.length > 0">
        <h5 v-if="v$.auth_data.username.$error">Логин:</h5>
        <p
          v-for="error of v$.auth_data.username.$errors"
          :key="error.$uid"
        >
          {{ error.$message }}
        </p>
        <h5 v-if="v$.auth_data.password.$error">Пароль:</h5>
        <p
          v-for="error of v$.auth_data.password.$errors"
          :key="error.$uid"
        >
          {{ error.$message }}
        </p>
        <h5 v-if="v$.auth_data.confirmPassword.$error">Пароль (повтор):</h5>
        <p
          v-for="error of v$.auth_data.confirmPassword.$errors"
          :key="error.$uid"
        >
          {{ error.$message }}
        </p>
      </div>


      <form @submit="submitHandler">
        <h1 class="h3 mb-3 fw-normal">Регистрация</h1>

        <div class="form-floating">
          <input
            type="text"
            class="form-control"
            placeholder="name@example.com"
            v-model="auth_data.username"
            required
          />
          <label>Логин</label>
        </div>
        <div class="form-floating">
          <input
            type="password"
            class="form-control"
            placeholder="Password"
            v-model="auth_data.password"
            required
            pattern="(?=.*[0-9])(?=.*[!@#$%^&*])(?=.*[a-z])(?=.*[A-Z])[0-9a-zA-Z!@#$%^&*]{6,}"
          />
          <label>Пароль</label>
        </div>
        <div class="form-floating">
          <input
            type="password"
            class="form-control"
            placeholder="Password"
            v-model="auth_data.confirmPassword"
            required
            pattern="(?=.*[0-9])(?=.*[!@#$%^&*])(?=.*[a-z])(?=.*[A-Z])[0-9a-zA-Z!@#$%^&*]{6,}"
          />
          <label>Повторите пароль</label>
        </div>
        <button class="w-100 btn btn-lg btn-primary" type="submit" :disabled="v$.$invalid">
          Регистрация
        </button>
        <br />
        <br />
        <p class="mt-5 mb-3 text-muted">&copy; Разработано ООИТ Академии МВД</p>
      </form>
    </main>
  </div>
</template>

<script>
import useVuelidate from "@vuelidate/core"
import { required, helpers, sameAs } from "@vuelidate/validators"

export default {
  name: "RegistrationView",
  data() {
    return {
      auth_data: {
        username: "levenko",
        password: "Minsk1986Minsk!",
        confirmPassword: "Minsk1986Minsk!"
      }
    }
  },
  setup() {
    return { v$: useVuelidate() }
  },
  validations() {
    const passwordRegex = helpers.regex(/(?=.*[0-9])(?=.*[!@#$%^&*])(?=.*[a-z])(?=.*[A-Z])[0-9a-zA-Z!@#$%^&*]{6,}/)
    const same = sameAs(this.auth_data.password)


    return {
      auth_data: {
        username: {
          required: helpers.withMessage("Поле не может быть пустым!", required),
          $autoDirty: true
        },
        password: {
          required: helpers.withMessage("Поле не может быть пустым!", required),
          passwordRegex: helpers.withMessage("Пароль не удовлетворяет минимальным требованиям безопасности!(пароль должен состоять из не менее 6 символов в которых должны присутствовать строчные, прописные буквы, цифры, спецсимволы)", passwordRegex),
          $autoDirty: true
        },
        confirmPassword: {
          $autoDirty: true,
          same: helpers.withMessage("Введенные пароли не совпадают!", same)
        }
      }
    }
  },
  methods: {
    submitHandler(e) {
      e.preventDefault()
      e.stopPropagation()
      if (!this.v$.$invalid) {
        this.$store
          .dispatch("auth/actionRegistration", { ...this.auth_data })
          .then((response) => {
            // console.log('resp', response.data())
            // this.$router.replace(this.$route.query.redirect || "/")
          })

      }
    }
  }
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
  border-top-left-radius: 0;
  border-top-right-radius: 0;
}
</style>
