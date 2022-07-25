import { createApp } from "vue"
import App from "./App.vue"
import router from "@/router/router"
import store from "@/store"

import { library } from "@fortawesome/fontawesome-svg-core"
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome"
import { faClone } from "@fortawesome/free-regular-svg-icons"
import { faTrashCan } from "@fortawesome/free-regular-svg-icons"
import { faCircleCheck } from "@fortawesome/free-regular-svg-icons"
import { faEye } from "@fortawesome/free-regular-svg-icons"
import { faPlusSquare } from "@fortawesome/free-solid-svg-icons"
import { faSquarePollVertical } from "@fortawesome/free-solid-svg-icons"
import Toast from "vue-toastification"
import "vue-toastification/dist/index.css"

library.add(faClone)
library.add(faTrashCan)
library.add(faCircleCheck)
library.add(faCircleCheck)
library.add(faEye)
library.add(faPlusSquare)
library.add(faSquarePollVertical)

createApp(App)
  .use(router)
  .use(store)
  .use(Toast)
  .component("font-awesome-icon", FontAwesomeIcon)
  .mount("#app")
