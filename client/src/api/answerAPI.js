import axios from "axios"
import { authHeaders } from "@/api/auth_api"

export const answerAPI = {
  async getAnswerData(token, answerId) {
    return axios.get(
      `${process.env.VUE_APP_BACKEND_PROTOCOL}://${process.env.VUE_APP_BACKEND_HOST}:${process.env.VUE_APP_BACKEND_PORT}/api/answers/${answerId}`,
      authHeaders(token)
    )
  },

  async updateAnswerData(token, answerData) {
    return axios.put(
      `${process.env.VUE_APP_BACKEND_PROTOCOL}://${process.env.VUE_APP_BACKEND_HOST}:${process.env.VUE_APP_BACKEND_PORT}/api/answers/${answerData.id}/`,
      answerData,
      authHeaders(token)
    )
  },

  async deleteAnswer(token, answerId) {
    return axios.delete(
      `${process.env.VUE_APP_BACKEND_PROTOCOL}://${process.env.VUE_APP_BACKEND_HOST}:${process.env.VUE_APP_BACKEND_PORT}/api/answers/${answerId}/`,
      authHeaders(token)
    )
  },
}
