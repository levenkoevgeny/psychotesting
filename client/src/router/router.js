import { createRouter, createWebHistory } from "vue-router"
import TestList from "@/components/psychotesting/TestList"
import TestQuestions from "@/components/psychotesting/TestQuestions"
import LoginView from "@/components/auth/LoginView"
import OrganisationData from "@/components/psychotesting/OrganisationData"
import RegistrationView from "@/components/auth/RegistrationView"
import NotFound from "@/components/common/NotFound"
import InternalServerError from "@/components/common/InternalServerError"

import store from "@/store"

const routes = [
  {
    path: "/",
    name: "main",
    redirect: "/tests",
  },
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
  { path: "/:pathMatch(.*)*", name: "NotFound", component: NotFound },
  { path: "/error", name: "error", component: InternalServerError },
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
    return {
      path: "/login",
      query: { redirect: to.fullPath },
    }
  }
})

export default router
