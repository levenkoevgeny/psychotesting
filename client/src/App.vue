<template>
  <CommonNav v-if="isLogged" />
  <div style="height: 70px" v-if="isLogged"></div>
  <router-view />
</template>

<script>
import CommonNav from "@/components/common/CommonNav"
import { mapState } from "vuex"


export default {
  components: { CommonNav },
  computed: mapState({
    isLogged: (state) => state.auth.isLoggedIn,
  }),
}
</script>
<style>

.test-data-top-border {
  border-top: 15px solid mediumpurple;
}

.component-left-border {
  border-left: 7px solid dodgerblue;
}

.component-white-background {
  background-color: white;
}
</style>
