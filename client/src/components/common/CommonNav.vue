<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-light" v-if="isLogged">
    <div class="container-fluid">
      <a class="navbar-brand" href="/" v-if="user">
        <img
          src="https://www.amia.by/favicon.ico"
          alt=""
          width="30"
          height="24"
          class="d-inline-block align-text-top"
        />
        {{ this.user.organization_name }}
      </a>
      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarNavDropdown"
        aria-controls="navbarNavDropdown"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarNavDropdown">
        <ul class="navbar-nav">
          <li class="nav-item">
            <router-link
              :to="{ name: 'main' }"
              class="nav-link active"
              aria-current="page"
              >На главную</router-link
            >
          </li>
          <li class="nav-item">
            <router-link
              :to="{ name: 'tests' }"
              class="nav-link"
              aria-current="page"
              >Мои тесты</router-link
            >
          </li>
          <li class="nav-item dropdown">
            <a
              class="nav-link dropdown-toggle"
              href="#"
              id="navbarDropdownMenuLink"
              role="button"
              data-bs-toggle="dropdown"
              aria-expanded="false"
            >
              Учетная запись
            </a>
            <ul class="dropdown-menu" aria-labelledby="navbarDropdownMenuLink">
              <li>
                <router-link
                  :to="{ name: 'personal-data' }"
                  class="dropdown-item"
                  aria-current="page"
                  >Персональные данные</router-link
                >
              </li>
              <li>
                <button class="dropdown-item" @click="this.logOut">
                  Выход из системы
                </button>
              </li>
            </ul>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script>
import { mapState, mapActions } from "vuex"
import router from "@/router/router"
export default {
  name: "CommonNav",
  computed: mapState({
    isLogged: (state) => state.auth.isLoggedIn,
    user: (state) => state.auth.user,
  }),
  methods: {
    logOut() {
      this["auth/actionRemoveLogIn"]()
      router.push({ name: "login" })
    },
    ...mapActions(["auth/actionRemoveLogIn"]),
  },
}
</script>

<style scoped></style>
