import Vue from 'vue';
import App from './App.vue';
import axios from 'axios'
import VueAxios from 'vue-axios'
import PrefixTitle from '@/components/PrefixTitle.vue';

Vue.config.productionTip = false;
Vue.use(VueAxios, axios)
Vue.component('prefix-title', PrefixTitle);

new Vue({
  render: h => h(App)
}).$mount('#app')
