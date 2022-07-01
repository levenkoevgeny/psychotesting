import { api } from "@/api/auth_api"
import {
  getLocalToken,
  saveLocalToken,
  removeLocalToken,
  saveLocalRefreshToken,
  getLocalRefreshToken,
  removeLocalRefreshToken,
} from "@/utils"
import router from "@/router/router"

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
    const data = await response.data
    saveLocalToken(data.access)
    saveLocalRefreshToken(data.refresh)
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
          const response = await api.getUserData(token)
          if (response.status >= 200 && response.status < 300) {
            const userData = await response.data
            commit("setLoggedIn", true)
            commit("setUserData", { ...userData })
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
