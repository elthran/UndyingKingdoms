import Vue from 'vue'
import VueRouter from 'vue-router'
// eslint-disable-next-line
import {customAxios, devLogin} from '@/assets/devHelpers.js'
import VueAxios from 'vue-axios'
import PrefixTitle from '@/components/PrefixTitle.vue'
import {APIInterfacePlugin} from '@/assets/APIInterfacePlugin.js'
import {routes} from '@/assets/routes.js'

import App from './App.vue'

// allows this.axios, which is an axios with custom config.
Vue.use(VueAxios, customAxios)
// allows this.$getData('/api/sidebar', this.$deployData)
Vue.use(APIInterfacePlugin)
Vue.use(VueRouter)

const router = new VueRouter({
  routes,
  base: '/m/',
  mode: 'history'
})

Vue.component('prefix-title', PrefixTitle)

const app = new Vue({
  router,
  render: h => h(App)
}).$mount('#app')
