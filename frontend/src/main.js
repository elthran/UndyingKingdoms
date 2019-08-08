import Vue from 'vue'
// eslint-disable-next-line
import http from '@/assets/http-helpers'  // devLogin runs immediately
import VueAxios from 'vue-axios'
import PrefixTitle from '@/components/PrefixTitle.vue'
import { APIInterfacePlugin } from '@/assets/api-interface-plugin'
import router from '@/assets/router.js'

import App from './App.vue'

// allows this.axios, which is an axios with custom config.
Vue.use(VueAxios, http)
// allows this.$hydrate('/api/navbar')
Vue.use(APIInterfacePlugin)

Vue.component('prefix-title', PrefixTitle)

const app = new Vue({
  router,
  render: h => h(App)
}).$mount('#app')
