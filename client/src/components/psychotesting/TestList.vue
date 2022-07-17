<template>
  <div v-if="isError" class="alert alert-danger m-0 p-3" role="alert">
    Ошибка загрузки данных!
  </div>
  <div class="container">
    <div
      class="my-3 p-3 rounded-3 component-white-background test-data-top-border d-flex flex-row justify-content-between"
    >
      <h1>Мои тесты</h1>
    </div>

    <div
      v-if="isLoading"
      class="d-flex justify-content-center align-items-center"
      style="height: 70vh"
    >
      <Spinner />
    </div>
    <div v-else class="mt-3">
      <div v-if="testList.length > 0">
        <div v-for="test in testList" :key="test.id">
          <TestItem
            :testData="test"
            @deleteTest="deleteTestHandler"
            @makeTestCopy="makeTestCopy"
          />
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
      isError: false,
    }
  },
  async created() {
    try {
      const response = await testDataAPI.getTestList(
        this.userToken,
        this.userData.id
      )
      this.testList = await response.data
    } catch (e) {
      this.isError = true
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
    async deleteTestHandler(testId) {
      try {
        this.isLoading = true
        await testDataAPI.deleteTestData(this.userToken, testId)
        this.testList = this.testList.filter((test) => test.id !== testId)
      } catch (e) {
        this.isError = true
      } finally {
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
      await this.$router.push({
        name: "test_questions",
        params: { id: newTest.id },
      })
    },
    async makeTestCopy(testId) {
      try {
        this.isLoading = true
        const response = await testDataAPI.makeTestCopy(this.userToken, testId)
        this.testList.push(response.data)
      } catch (error) {
      } finally {
        this.isLoading = false
      }
    },
  },
}
</script>

<style scoped></style>
