import { api } from "@/api/auth_api"
import {
  getLocalToken,
  saveLocalToken,
  removeLocalToken,
  getLocalUserId,
  saveLocalUserId,
  removeLocalUserId,
} from "@/utils"

const state = () => ({
  token: null,
  isLoggedIn: null,
  logInError: false,
  user: null,
})

// getters
const getters = {
  getToken(state) {
    return state.token
  },
  getIsLoggedIn(state) {
    return state.isLoggedIn
  },
  getLogInError(state) {
    return state.logInError
  },
  getUser(state) {
    return state.user
  },
}

// actions
const actions = {
  async actionLogIn({ commit }, payload) {
    let { username, password } = payload
    const response = await api.logInGetToken(username, password)
    const data = await response.json()
    console.log("data", data)
    saveLocalToken(data.token)
    saveLocalUserId(data.user_id)
  },

  async actionCheckLoggedIn({ state, commit, dispatch }) {
    if (!state.isLoggedIn) {
      let token = state.token
      if (!token) {
        const localToken = getLocalToken()
        if (localToken) {
          commit("setToken", localToken)
          token = localToken
        }
      }
      if (token) {
        try {
          const response = await api.getUserData(token, getLocalUserId())

          if (response.status >= 200 && response.status < 300) {
            console.log(response.status)
            const userData = await response.json()
            commit("setLoggedIn", true)
            commit("setUserData", { ...userData[0] })
          } else {
            throw new Error("User data error")
          }
        } catch (error) {
          dispatch("actionRemoveLogIn")
        }
      } else {
        dispatch("actionRemoveLogIn")
      }
    }
  },

  async actionRemoveLogIn({ state, commit }) {
    removeLocalToken()
    removeLocalUserId()
    commit("setToken", "")
    commit("setLoggedIn", false)
  },
}

// mutations
const mutations = {
  setLoggedIn(state, payload) {
    state.isLoggedIn = payload
  },
  setToken(state, payload) {
    state.token = payload
  },
  setUserData(state, payload) {
    state.user = payload
  },
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
}
