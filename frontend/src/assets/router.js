import Vue from 'vue'
import VueRouter from 'vue-router'

// you don't need to use this, just put all chunked files in here.
// NOTE: chunking only works if the component is also async
import '@/assets/chunks.js'
import LoadingComponent from '@/components/LoadingComponent.vue'
import ErrorComponent from '@/components/ErrorComponent.vue'
import OverviewApp from '@/overview/OverviewApp.vue'
import InfrastructureApp from '@/infrastructure/InfrastructureApp.vue'
const AsyncChatroomApp = () => ({
  // The component to load (should be a Promise)
  component: import(/* webpackChunkName: "ChatroomApp" */ '@/chatroom/ChatroomApp.vue'),
  // A component to use while the async component is loading
  loading: LoadingComponent,
  // A component to use if the load fails
  error: ErrorComponent,
  // Delay before showing the loading component. Default: 200ms.
  delay: 50,
  // The error component will be displayed if a timeout is
  // provided and exceeded. Default: Infinity.
  timeout: 3000
})
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
      component: AsyncChatroomApp
    },
    {
      path: '/user/forum/:thread_id/:post_id',
      name: 'ForumApp',
      component: ForumApp
    },
  ],
  base: '/m/',
  mode: 'history'
})
