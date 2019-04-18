import Vue from 'vue'
import VueRouter from 'vue-router'

// you don't need to use this, just put all chunked files in here.
// NOTE: chunking only works if the component is also async
import '@/assets/chunks.js'
import OverviewApp from '@/overview/OverviewApp.vue'
import InfrastructureApp from '@/infrastructure/InfrastructureApp.vue'
const ChatroomApp = () => import(/* webpackChunkName: "ChatroomApp" */ '@/chatroom/ChatroomApp.vue')
import ForumApp from '@/forum/ForumApp.vue'

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
    },
    {
      path: '/user/forum',
      name: 'ForumApp',
      component: ForumApp
    },
  ],
  base: '/m/',
  mode: 'history'
})
