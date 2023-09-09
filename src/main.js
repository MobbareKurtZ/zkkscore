import { createApp } from 'vue'
import App from './App.vue'

import { library } from '@fortawesome/fontawesome-svg-core'

import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

import { faCoffee, faMugHot } from '@fortawesome/free-solid-svg-icons'

library.add(faCoffee, faMugHot);

createApp(App).mount('#app')
