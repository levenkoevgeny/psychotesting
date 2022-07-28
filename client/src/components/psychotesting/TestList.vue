<template>
  <div v-if="isError" class="alert alert-danger m-0 p-3" role="alert">
    Что-то пошло не так!
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
      <div v-if="getTestListLength > 0">
        <div v-for="test in sortedTests" :key="test.id">
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
import { useToast } from "vue-toastification"

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
  setup() {
    const toast = useToast()
    return { toast }
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
    getTestListLength: function () {
      return this.testList.length
    },
    sortedTests: function () {
      return this.testList.sort(function (a, b) {
        if (a.index_number < b.index_number) {
          return -1
        }
        if (a.index_number > b.index_number) {
          return 1
        }
        return 0
      })
    },
  },
  methods: {
    arrangeIndexAdd(after) {
      this.testList.map((test) => {
        if (parseInt(test.index_number) > parseInt(after)) {
          test.index_number = test.index_number + 1
        }
      })
    },
    arrangeIndexDelete(after) {
      this.testList.map((test) => {
        if (parseInt(test.index_number) > parseInt(after)) {
          test.index_number = test.index_number - 1
        }
      })
    },
    async addNewTestHandler() {
      this.isLoading = true
      try {
        const response = await testDataAPI.addNewTest(
          this.userToken,
          {
            test_name: "Новый тест",
            extra_data: "описание",
            is_active: false,
            organization: this.userData.id,
          },
          this.getTestListLength
        )
        const newTest = await response.data
        await this.$router.push({
          name: "test_questions",
          params: { id: newTest.id },
        })
      } catch (e) {
        this.isError = true
      }
    },
    async makeTestCopy(testId, afterNumber) {
      this.isLoading = true
      try {
        const response = await testDataAPI.makeTestCopy(this.userToken, testId)
        this.arrangeIndexAdd(afterNumber)
        this.testList.push(response.data)
      } catch (error) {
        this.isError = true
      } finally {
        this.isLoading = false
      }
    },
    async deleteTestHandler(testId, afterNumber) {
      this.isLoading = true
      try {
        await testDataAPI.deleteTestData(this.userToken, testId)
        this.testList = this.testList.filter((test) => test.id !== testId)
        this.arrangeIndexDelete(afterNumber)
      } catch (e) {
        this.isError = true
      } finally {
        this.toast.warning("Тест удален!", {
          timeout: 700,
          closeOnClick: true,
        })
        this.isLoading = false
      }
    },
  },
}
</script>

<style scoped></style>
