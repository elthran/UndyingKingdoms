import Vue from 'vue'
import VueRouter from 'vue-router'

import InfrastructureApp from '@/infrastructure/InfrastructureApp.vue'
import OverviewApp from '@/overview/OverviewApp.vue'


Vue.use(VueRouter)

export default new VueRouter({
  routes: [  // probably should generate these from an api call?
    {
      path: '/gameplay/infrastructure',
      name: 'InfrastructureApp',
      component: InfrastructureApp
    },
    {
      path: '/gameplay/overview',
      name: 'OverviewApp',
      component: OverviewApp
    }
  ],
  base: '/m/',
  mode: 'history'
})
