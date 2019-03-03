<template>
  <div id="infrastructure-app">
    <prefix-title title="City Planner" />
    <resource-header />
    <!-- <economy-form /> -->
    <nav-bar />
  </div>
</template>

<script>
import NavBar from '@/components/NavBar.vue'
import ResourceHeader from './ResourceHeader.vue'
// import EconomyForm from './EconomyForm.vue'

export default {
  name: 'InfrastructureApp',
  components: {
    'nav-bar': NavBar,
    'resource-header': ResourceHeader
    // 'economy-form': EconomyForm
  }
}
</script>

<style scoped>
#infrastructure-app {
  margin: 1em 1em 0.6em;
}
</style>
