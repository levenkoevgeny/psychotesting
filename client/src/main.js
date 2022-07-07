import { createApp } from "vue"
import App from "./App.vue"
import router from "@/router/router"
import store from "@/store"

import { library } from "@fortawesome/fontawesome-svg-core"
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome"
import { faClone } from "@fortawesome/free-regular-svg-icons"
import { faTrashCan } from "@fortawesome/free-regular-svg-icons"
import { faCircleCheck } from "@fortawesome/free-regular-svg-icons"
import { faPlusCircle } from "@fortawesome/free-solid-svg-icons"

library.add(faClone)
library.add(faTrashCan)
library.add(faCircleCheck)
library.add(faCircleCheck)

createApp(App)
  .use(router)
  .use(store)
  .component("font-awesome-icon", FontAwesomeIcon)
  .mount("#app")
