<template>
  <div v-if="isRegistrationError" class="alert alert-danger m-0 p-3" role="alert">
    Ошибка регистрации!
  </div>
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


      <form @submit.prevent="submitHandler">
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
            class="form-control form-password"
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
            class="form-control form-password-confirm"
            placeholder="Password"
            v-model="auth_data.confirmPassword"
            required
            pattern="(?=.*[0-9])(?=.*[!@#$%^&*])(?=.*[a-z])(?=.*[A-Z])[0-9a-zA-Z!@#$%^&*]{6,}"
          />
          <label>Повторите пароль</label>
        </div>
        <button v-if="v$.$pending" class="w-100 btn btn-lg btn-primary mt-2" type="submit" :disabled="dataIsValid">
          Проверка ...
        </button>
        <button v-else class="w-100 btn btn-lg btn-primary mt-2" type="submit" :disabled="dataIsValid">
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
import { mapGetters } from "vuex"
import { api } from "@/api/auth_api"

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
  computed: {
    ...mapGetters({
      isRegistrationError: "auth/getIsRegistrationError"
    }),
    dataIsValid: function() {
      if (this.v$.$pending) {
        return true
      } else return this.v$.$invalid
    }
  },
  setup() {
    return { v$: useVuelidate() }
  },
  validations() {
    const passwordRegex = helpers.regex(/(?=.*[0-9])(?=.*[!@#$%^&*])(?=.*[a-z])(?=.*[A-Z])[0-9a-zA-Z!@#$%^&*]{6,}/)
    const loginRegex = helpers.regex(/^[a-zA-Z\d]*$/)
    const same = sameAs(this.auth_data.password)
    const isUserNameTaken = helpers.withAsync(async (value) => {
      if (value === '') return true
      const response = await api.getUserNames(value)
      return new Promise((resolve, reject) => {setTimeout(()=> resolve(response.data.length <= 0), 1000)})
      // return response.data.length <= 0;
    })

    return {
      auth_data: {
        username: {
          required: helpers.withMessage("Поле не может быть пустым", required),
          isUnique: helpers.withMessage('Пользователь с таким именем уже присутствует в системе', isUserNameTaken),
          loginRegex: helpers.withMessage('Допускаются только латинские буквы', loginRegex),
          $autoDirty: true
        },
        password: {
          required: helpers.withMessage("Поле не может быть пустым", required),
          passwordRegex: helpers.withMessage("Пароль не удовлетворяет минимальным требованиям безопасности (пароль должен состоять из не менее 6 символов в которых должны присутствовать строчные, прописные буквы, цифры, спецсимволы)", passwordRegex),
          $autoDirty: true
        },
        confirmPassword: {
          $autoDirty: true,
          same: helpers.withMessage("Введенные пароли не совпадают", same)
        }
      }
    }
  },
  methods: {
    submitHandler(e) {
      if (!this.v$.$invalid) {
        this.$store.dispatch("auth/actionRegistration", { ...this.auth_data })
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

.form-password {
  border-radius: 0;
  margin-bottom: -1px;
}

.form-password-confirm {
    border-top-left-radius: 0;
    border-top-right-radius: 0;
}

</style>
