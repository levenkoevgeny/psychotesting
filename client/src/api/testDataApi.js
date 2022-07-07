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

  async addNewTest(token, testData) {
    return axios.post(
      `${process.env.VUE_APP_BACKEND_PROTOCOL}://${process.env.VUE_APP_BACKEND_HOST}:${process.env.VUE_APP_BACKEND_PORT}/api/test-data/`,
      testData,
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
