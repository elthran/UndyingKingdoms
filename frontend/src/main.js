import Vue from 'vue'
import App from './App.vue'
import titleComponent from './components/Title.vue';
Vue.component('vue-title', titleComponent);

Vue.config.productionTip = false

new Vue({
  render: h => h(App),
}).$mount('#app')
