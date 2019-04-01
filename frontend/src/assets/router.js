import Vue from 'vue'
import VueRouter from 'vue-router'

import OverviewApp from '@/overview/OverviewApp.vue'
import InfrastructureApp from '@/infrastructure/InfrastructureApp.vue'
import ChatroomApp from '@/chatroom/ChatroomApp.vue'

Vue.use(VueRouter)

export default new VueRouter({
  routes: [  // probably should generate these from an api call?
    {
      path: '/gameplay/overview',
      name: 'OverviewApp',
      component: OverviewApp
    },
    {
      path: '/gameplay/infrastructure',
      name: 'InfrastructureApp',
      component: InfrastructureApp
    },
    {
      path: '/gameplay/chatroom',
      name: 'ChatroomApp',
      component: ChatroomApp
    }
  ],
  base: '/m/',
  mode: 'history'
})
