import axios from "axios"
import { authHeaders } from "@/api/auth_api"

export const questionsAPI = {
  async getQuestionsByTest(token, testId) {
    return axios.get(
      `${process.env.VUE_APP_BACKEND_PROTOCOL}://${process.env.VUE_APP_BACKEND_HOST}:${process.env.VUE_APP_BACKEND_PORT}/api/questions/?test_id=${testId}`,
      authHeaders(token)
    )
  },

  async getQuestionsByTestForRunning(testId) {
    return axios.get(
      `${process.env.VUE_APP_BACKEND_PROTOCOL}://${process.env.VUE_APP_BACKEND_HOST}:${process.env.VUE_APP_BACKEND_PORT}/api/questions/?test_id=${testId}`
    )
  },

  async addNewQuestion(token, questionData, afterNumber) {
    return axios.post(
      `${process.env.VUE_APP_BACKEND_PROTOCOL}://${process.env.VUE_APP_BACKEND_HOST}:${process.env.VUE_APP_BACKEND_PORT}/api/questions/?after=${afterNumber}`,
      questionData,
      authHeaders(token)
    )
  },
  async makeQuestionCopy(token, questionId) {
    return axios.post(
      `${process.env.VUE_APP_BACKEND_PROTOCOL}://${process.env.VUE_APP_BACKEND_HOST}:${process.env.VUE_APP_BACKEND_PORT}/api/questions/${questionId}/make_copy/`,
      null,
      authHeaders(token)
    )
  },
  async deleteQuestionAnswers(token, questionId) {
    return axios.post(
      `${process.env.VUE_APP_BACKEND_PROTOCOL}://${process.env.VUE_APP_BACKEND_HOST}:${process.env.VUE_APP_BACKEND_PORT}/api/questions/${questionId}/delete_all_answers/`,
      null,
      authHeaders(token)
    )
  },
  async deleteQuestion(token, questionId) {
    return axios.delete(
      `${process.env.VUE_APP_BACKEND_PROTOCOL}://${process.env.VUE_APP_BACKEND_HOST}:${process.env.VUE_APP_BACKEND_PORT}/api/questions/${questionId}/`,
      authHeaders(token)
    )
  },
  async updateQuestion(token, questionData) {
    return axios.put(
      `${process.env.VUE_APP_BACKEND_PROTOCOL}://${process.env.VUE_APP_BACKEND_HOST}:${process.env.VUE_APP_BACKEND_PORT}/api/questions/${questionData.id}/`,
      questionData,
      authHeaders(token)
    )
  },
}
