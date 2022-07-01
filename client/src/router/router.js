import { createRouter, createWebHistory } from "vue-router"
import TestList from "@/components/psychotesting/TestList"
import TestQuestions from "@/components/psychotesting/TestQuestions"
import LoginView from "@/components/auth/LoginView"
import OrganisationData from "@/components/psychotesting/OrganisationData"
import RegistrationView from "@/components/auth/RegistrationView"

import store from "@/store"

const routes = [
  {
    path: "/tests",
    name: "tests",
    component: TestList,
    meta: { requiresAuth: true },
  },
  {
    path: "/tests/:id",
    name: "test_questions",
    component: TestQuestions,
    meta: { requiresAuth: true },
  },
  // { path: "/words", name: "words", component: WordsList },
  {
    path: "/login",
    name: "login",
    component: LoginView,
    meta: { requiresAuth: false },
  },
  {
    path: "/registration",
    name: "registration",
    component: RegistrationView,
    meta: { requiresAuth: false },
  },
  {
    path: "/personal-data",
    name: "personal-data",
    component: OrganisationData,
    meta: { requiresAuth: true },
  },
  // { path: "/registration", name: "registration", component: RegistrationView },
]

const router = createRouter({
  routes,
  history: createWebHistory(process.env.BASE_URL),
})

const isAuthenticated = true

router.beforeEach(async (to, from) => {
  await store.dispatch("auth/actionCheckLoggedIn")
  const isLoggedIn = store.getters["auth/getIsLoggedIn"]

  if (to.meta.requiresAuth && !isLoggedIn) {
    // this route requires auth, check if logged in
    // if not, redirect to login page.
    return {
      path: "/login",
      // save the location we were at to come back later
      query: { redirect: to.fullPath },
    }
  }
})

export default router
