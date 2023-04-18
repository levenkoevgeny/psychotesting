import axios from "axios"
import { authHeaders } from "@/api/auth_api"

export const testDataAPI = {
  async getTestList(token, userId) {
    return axios.get(
      `${process.env.VUE_APP_BACKEND_PROTOCOL}://${process.env.VUE_APP_BACKEND_HOST}:${process.env.VUE_APP_BACKEND_PORT}/api/test-data/?organization_id=${userId}`,
      authHeaders(token)
    )
  },

  async getTestData(token, testId) {
    return axios.get(
      `${process.env.VUE_APP_BACKEND_PROTOCOL}://${process.env.VUE_APP_BACKEND_HOST}:${process.env.VUE_APP_BACKEND_PORT}/api/test-data/${testId}/`,
      authHeaders(token)
    )
  },

  async getTestDataForRunning(testId) {
    return axios.get(
      `${process.env.VUE_APP_BACKEND_PROTOCOL}://${process.env.VUE_APP_BACKEND_HOST}:${process.env.VUE_APP_BACKEND_PORT}/api/test-data/${testId}/`
    )
  },

  async getTestDataResultFullText(token, testId) {
    return axios.post(
      `${process.env.VUE_APP_BACKEND_PROTOCOL}://${process.env.VUE_APP_BACKEND_HOST}:${process.env.VUE_APP_BACKEND_PORT}/api/test-data/${testId}/results_full_text/`,
      {},
      authHeaders(token)
    )
  },

  async getTestDataResultIndex(token, testId) {
    return axios.post(
      `${process.env.VUE_APP_BACKEND_PROTOCOL}://${process.env.VUE_APP_BACKEND_HOST}:${process.env.VUE_APP_BACKEND_PORT}/api/test-data/${testId}/results_index/`,
      {},
      authHeaders(token)
    )
  },

  async getTestDataResultAnswersCount(token, testId) {
    return axios.post(
      `${process.env.VUE_APP_BACKEND_PROTOCOL}://${process.env.VUE_APP_BACKEND_HOST}:${process.env.VUE_APP_BACKEND_PORT}/api/test-data/${testId}/results_answers_count/`,
      {},
      authHeaders(token)
    )
  },

  async getTestDataResult_1_0(token, testId) {
    return axios.post(
      `${process.env.VUE_APP_BACKEND_PROTOCOL}://${process.env.VUE_APP_BACKEND_HOST}:${process.env.VUE_APP_BACKEND_PORT}/api/test-data/${testId}/results_answers_1_0/`,
      {},
      authHeaders(token)
    )
  },

  async addNewTest(token, testData, afterNumber) {
    return axios.post(
      `${process.env.VUE_APP_BACKEND_PROTOCOL}://${process.env.VUE_APP_BACKEND_HOST}:${process.env.VUE_APP_BACKEND_PORT}/api/test-data/?after=${afterNumber}`,
      testData,
      authHeaders(token)
    )
  },

  async makeTestCopy(token, testId) {
    return axios.post(
      `${process.env.VUE_APP_BACKEND_PROTOCOL}://${process.env.VUE_APP_BACKEND_HOST}:${process.env.VUE_APP_BACKEND_PORT}/api/test-data/${testId}/make_copy/`,
      null,
      authHeaders(token)
    )
  },

  async updateTestData(token, testData) {
    return axios.put(
      `${process.env.VUE_APP_BACKEND_PROTOCOL}://${process.env.VUE_APP_BACKEND_HOST}:${process.env.VUE_APP_BACKEND_PORT}/api/test-data/${testData.id}/`,
      testData,
      authHeaders(token)
    )
  },

  async deleteTestData(token, testId) {
    return axios.delete(
      `${process.env.VUE_APP_BACKEND_PROTOCOL}://${process.env.VUE_APP_BACKEND_HOST}:${process.env.VUE_APP_BACKEND_PORT}/api/test-data/${testId}/`,
      authHeaders(token)
    )
  },
}
