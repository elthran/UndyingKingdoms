import Vue from 'vue'
import InfrastructureApp from './InfrastructureApp.vue'
// eslint-disable-next-line
import {customAxios, devLogin} from '@/assets/devHelpers.js'
import VueAxios from 'vue-axios'
import PrefixTitle from '@/components/PrefixTitle.vue'
import {APIInterfacePlugin} from '@/assets/APIInterfacePlugin.js'

Vue.use(VueAxios, customAxios)  // allows this.axios, which is an axios with custom config.
Vue.use(APIInterfacePlugin)
Vue.component('prefix-title', PrefixTitle)

new Vue({
  render: h => h(InfrastructureApp)
}).$mount('#app')

export default {
  name: 'main',
  data () {
    return {
      errors: Object
    }
  }
}
