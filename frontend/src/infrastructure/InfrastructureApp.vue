<template>
  <div id="infrastructure-app">
    <prefix-title title="City Planner" />
    <resource-header />
    <div class="bottom-spacer-1" />
    <nav-bar />
  </div>
</template>

<script>
import NavBar from '@/components/NavBar.vue'
import ResourceHeader from './ResourceHeader.vue'

export default {
  name: 'InfrastructureApp',
  components: {
    'nav-bar': NavBar,
    'resource-header': ResourceHeader
  }
}
</script>

<style scoped>
#infrastructure-app {
  margin: 1em 1em 0.6em;
}
</style>
