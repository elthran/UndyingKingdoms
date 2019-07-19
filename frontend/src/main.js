import Vue from 'vue'
// eslint-disable-next-line
import {customAxios, devLogin} from '@/assets/devHelpers.js'  // devLogin runs immediately
import VueAxios from 'vue-axios'
import PrefixTitle from '@/components/PrefixTitle.vue'
import {APIInterfacePlugin} from '@/assets/APIInterfacePlugin.js'
import router from '@/assets/router.js'

import App from './App.vue'

// allows this.axios, which is an axios with custom config.
Vue.use(VueAxios, customAxios)
// allows this.$hydrate('/api/navbar')
Vue.use(APIInterfacePlugin)

Vue.component('prefix-title', PrefixTitle)

const app = new Vue({
  router,
  render: h => h(App)
}).$mount('#app')
