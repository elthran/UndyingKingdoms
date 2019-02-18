import Vue from 'vue';
import EconomyApp from './EconomyApp.vue';
// eslint-disable-next-line
import {customAxios, devLogin} from '@/assets/devHelpers.js'
import VueAxios from 'vue-axios';
import PrefixTitle from '@/components/PrefixTitle.vue';

Vue.use(VueAxios, customAxios);
Vue.component('prefix-title', PrefixTitle);

new Vue({
    render: h => h(EconomyApp)
}).$mount('#app');

export default {
	name: 'main',
	data () {
	}
}
