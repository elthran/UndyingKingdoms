import Vue from 'vue';
import EconomyApp from './EconomyApp.vue';
import axios from 'axios';
import VueAxios from 'vue-axios';
import PrefixTitle from '@/components/PrefixTitle.vue';

Vue.use(VueAxios, axios);
Vue.component('prefix-title', PrefixTitle);

new Vue({
		delimiters: ['v{', '}'],
    render: h => h(EconomyApp)
}).$mount('#app');

export default {
	name: 'main',
	data () {
	}
}
