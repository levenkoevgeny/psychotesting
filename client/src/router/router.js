import { createRouter, createWebHistory } from "vue-router"
import TestList from "@/components/psychotesting/TestList"
import TestQuestions from "@/components/psychotesting/TestQuestions"
import LoginView from "@/components/auth/LoginView"

const routes = [
  { path: "/tests", name: "tests", component: TestList },
  { path: "/tests/:id", name: "test_questions", component: TestQuestions },
  // { path: "/words", name: "words", component: WordsList },
  { path: "/login", name: "login", component: LoginView },
  // { path: "/registration", name: "registration", component: RegistrationView },
]

const router = createRouter({
  routes,
  history: createWebHistory(process.env.BASE_URL),
})

const isAuthenticated = true

router.beforeEach(async (to, from) => {
  console.log("before router")
  if (!isAuthenticated && to.name !== "login") {
    return { name: "login" }
  }
})

export default router
