<template>
  <div class="container">
    <div
      class="my-3 p-3 rounded-3 component-white-background test-data-top-border d-flex flex-row justify-content-between"
    >
      <h1>Мои тесты</h1>
    </div>

    <div v-if="isLoading" class="mt-3">
      <Spinner />
    </div>
    <div v-else class="mt-3">
      <div v-if="testList.length > 0">
        <div v-for="(test, index) in testList" :key="test.id">
          <TestItem :test-data="test" @deleteTest="deleteTestHandler" />
        </div>
      </div>
    </div>
    <div class="fixed-bottom m-3" style="display: inline; !important;">
      <button
        type="button"
        class="btn btn-light rounded-circle fs-2"
        @click="addNewTestHandler"
      >
        <font-awesome-icon icon="fa-solid fa-circle-plus" />
      </button>
    </div>
  </div>
</template>

<script>
import Spinner from "@/components/common/Spinner"
import TestItem from "@/components/psychotesting/TestItem"
import { mapGetters } from "vuex"
import { testDataAPI } from "@/api/testDataApi"
import router from "@/router/router"
export default {
  name: "TestList",
  components: { Spinner, TestItem },
  data() {
    return {
      newTestData: {
        test_name: "",
      },
      testList: [],
      isLoading: true,
    }
  },
  async created() {
    try {
      const response = await testDataAPI.getTestList(
        this.userToken,
        this.userData.id
      )
      const data = await response.data
      this.testList = data
    } catch (e) {
      console.log(e.message)
    } finally {
      this.isLoading = false
    }
  },
  computed: {
    ...mapGetters({
      userData: "auth/getUser",
      userToken: "auth/getToken",
    }),
  },
  methods: {
    deleteTestHandler(testId) {
      try {
        this.isLoading = true
        testDataAPI.deleteTestData(this.userToken, testId)
      } catch (e) {
      } finally {
        this.testList = this.testList.filter((test) => test.id !== testId)
        this.isLoading = false
      }
    },
    async addNewTestHandler() {
      this.isLoading = true
      const response = await testDataAPI.addNewTest(this.userToken, {
        test_name: "Новый тест",
        extra_data: "описание",
        is_active: false,
        organization: this.userData.id,
      })
      const newTest = await response.data
      this.isLoading = false
      router.push({ name: "test_questions", params: { id: newTest.id } })
    },
  },
}
</script>

<style scoped></style>
