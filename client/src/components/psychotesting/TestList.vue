<template>
  <div class="container">
    <div
      class="my-3 p-3 rounded-3 component-white-background test-data-top-border"
    >
      <h1>Test list</h1>
    </div>

    <div v-if="isLoading" class="mt-3">
      <Spinner />
    </div>
    <div v-else class="mt-3">
      <div v-if="testList.length > 0">
        <div
          v-for="(test, index) in testList"
          :key="test.id"
          class="my-3 p-3 rounded-3 component-white-background component-left-border"
        >
          <router-link
            :to="{ name: 'test_questions', params: { id: test.id } }"
          >
            <h5>{{ test.test_name }}</h5>
          </router-link>
          <small>Количество вопросов - 00</small><br />
          <small>Дата создания - {{ test.data_created }}</small>
        </div>
      </div>
      <div v-else>Список пуст</div>
    </div>
  </div>
</template>

<script>
import Spinner from "@/components/common/Spinner"
import { mapGetters } from "vuex"
export default {
  name: "TestList",
  components: { Spinner },
  data() {
    return {
      newTestData: {
        test_name: "",
      },
      testList: [],
      isLoading: true,
    }
  },
  created() {
    fetch(
      `${process.env.VUE_APP_BACKEND_PROTOCOL}://${process.env.VUE_APP_BACKEND_HOST}:${process.env.VUE_APP_BACKEND_PORT}/api/test-data/?organization_id=${this.userData.id}`
    )
      .then((response) => response.json())
      .then((tests) => {
        this.testList = tests
      })
      .catch((e) => alert(e))
      .finally(() => (this.isLoading = false))
  },
  computed: {
    ...mapGetters({
      userData: "auth/getUser",
    }),
  },
}
</script>

<style scoped></style>
