import Vue from 'vue'
import EconomyApp from './EconomyApp.vue'
// eslint-disable-next-line
import http from '@/assets/http-helpers'
import VueAxios from 'vue-axios'
import PrefixTitle from '@/components/PrefixTitle.vue'
import {APIInterfacePlugin} from '@/assets/api-interface-plugin'

Vue.use(VueAxios, http)  // allows this.axios, which is an axios with custom config.
Vue.use(APIInterfacePlugin)
Vue.component('prefix-title', PrefixTitle)

new Vue({
  render: h => h(EconomyApp)
}).$mount('#app')

export default {
  name: 'main',
  data () {
    return {
      errors: Object
    }
  }
}
