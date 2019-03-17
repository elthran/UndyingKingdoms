import InfrastructureApp from '@/infrastructure/InfrastructureApp.vue'
import OverviewApp from '@/overview/OverviewApp.vue'


// probably should generate these from an api call?
export const routes = [
  {path: '/gameplay/infrastructure', component: InfrastructureApp},
  {path: '/gameplay/overview', component: OverviewApp }
]
