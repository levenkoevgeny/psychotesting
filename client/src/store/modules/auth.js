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
  isLogInError: null,
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
  getIsLogInError(state) {
    return state.isLogInError
  },
  getUser(state) {
    return state.user
  },
}

// actions
const actions = {
  async actionLogIn({ commit }, payload) {
    try {
      let { username, password } = payload
      const response = await api.logInGetToken(username, password)
      const data = await response.data
      const token = data.access
      const refresh = data.refresh
      if (token) {
        saveLocalToken(token)
        saveLocalRefreshToken(refresh)
        commit("setToken", token)
        commit("setLoggedIn", true)
        commit("setIsLogInError", false)
        const response = await api.getUserData(token)
        const userData = await response.data
        commit("setUserData", { ...userData })
      }
    } catch (error) {
      commit("setIsLogInError", true)
    }
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
          const userData = await response.data
          commit("setUserData", { ...userData })
          commit("setLoggedIn", true)
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

  async updateUserData({ state, commit }, payload) {
    // добавить код
    commit("setUserData", { ...payload })
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
  setIsLogInError(state, payload) {
    state.isLogInError = payload
  },
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
}
