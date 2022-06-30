import { api } from "@/api/auth_api"
import { getLocalToken, saveLocalToken, removeLocalToken } from "@/utils"

const state = () => ({
  token: null,
  isLoggedIn: false,
  user: { id: null, is_superuser: false, lastname: null },
})

// getters
const getters = {
  getLastName(state) {
    return state.user.lastname
  },
}

// actions
const actions = {
  async actionLogIn({ commit }, payload) {
    let { username, password } = payload
    const response = await api.logInGetToken(username, password)
    const data = await response.json()
    saveLocalToken(data.token)
  },
  // async getAllProducts ({ commit }) {
  //     const products = await shop.getProducts()
  //     commit('setProducts', products)
  // }
}

// mutations
const mutations = {
  // setProducts (state, products) {
  //     state.all = products
  // },
  //
  // decrementProductInventory (state, { id }) {
  //     const product = state.all.find(product => product.id === id)
  //     product.inventory--
  // }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
}
