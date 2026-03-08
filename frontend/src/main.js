import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
import { library } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

/* 사용할 아이콘들을 불러오기 (예: home, user, file, briefcase) */
import { faHome, faUser, faFileLines, faBriefcase, faRightFromBracket, faGear, faRightToBracket, faFileShield, faArrowLeft } from '@fortawesome/free-solid-svg-icons'

/* 라이브러리에 아이콘 추가 */
library.add(faHome, faUser, faFileLines, faBriefcase, faGear, faRightFromBracket, faRightToBracket, faFileShield, faArrowLeft)

const app = createApp(App)

app.component('font-awesome-icon', FontAwesomeIcon)
app.use(createPinia())
app.use(router)

app.mount('#app')
