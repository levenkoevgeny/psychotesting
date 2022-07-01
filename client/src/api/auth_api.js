import axios from "axios"

function authHeaders(token) {
  return {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  }
}


axios.interceptors.response.use(function(response){
  console.log('inter success')
  return response
}, function(error){
  console.log('inter error')
  console.log(error.response.status)
  return Promise.reject(error);
})




export const api = {
  async logInGetToken(username, password) {
    const params = new URLSearchParams()
    params.append("username", username)
    params.append("password", password)

    return axios.post(
      `${process.env.VUE_APP_BACKEND_PROTOCOL}://${process.env.VUE_APP_BACKEND_HOST}:${process.env.VUE_APP_BACKEND_PORT}/api/token/`,
      params
    )
  },
  async getUserData(token) {
    return axios.get(`${process.env.VUE_APP_BACKEND_PROTOCOL}://${process.env.VUE_APP_BACKEND_HOST}:${process.env.VUE_APP_BACKEND_PORT}/api/users/me/`, authHeaders(token))
  },
}
