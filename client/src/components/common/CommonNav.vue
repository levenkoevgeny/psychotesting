<template>
  <nav class="nav justify-content-center" style="background-color: white">
    <button
      class="btn btn-link"
      aria-current="page"
      @click="$router.push({ name: 'tests' })"
    >
      Мои тесты
    </button>
    <div class="dropdown">
      <div v-if="isLogged">
        <button
          class="btn btn-secondary dropdown-toggle"
          type="button"
          id="dropdownMenuButton1"
          data-bs-toggle="dropdown"
          aria-expanded="false"
        >
          {{ this.user.organization_name }}
        </button>
        <ul class="dropdown-menu" aria-labelledby="dropdownMenuButton1">
          <li>
            <a class="dropdown-item" @click="this.logOut">Выйти из системы</a>
          </li>
          <li>
            <a
              class="dropdown-item"
              @click="$router.push({ name: 'personal-data' })"
              >Настройки</a
            >
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
    ...mapActions([
      "auth/actionRemoveLogIn", // map `this.increment()` to `this.$store.dispatch('increment')`
    ]),
  },
}
</script>

<style scoped></style>
