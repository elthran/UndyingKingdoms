<style scoped>
#infrastructure-app {
  margin: 1em 1em 0.6em;
}
</style>
<template>
  <div id="infrastructure-app">
    <prefix-title title="City Planner" />
    <resource-header>
      <idle-population-form />
    </resource-header>
    <div class="bottom-spacer-dot-6" />
    <building-selector />
    <div class="bottom-spacer-1" />
    <nav-bar />
  </div>
</template>

<script>
import NavBar from '@/components/NavBar.vue'
import ResourceHeader from './ResourceHeader.vue'
import IdlePopulationForm from './IdlePopulationForm.vue'
import BuildingSelector from './BuildingSelector.vue'

export default {
  name: 'InfrastructureApp',
  components: {
    'nav-bar': NavBar,
    'resource-header': ResourceHeader,
    'idle-population-form': IdlePopulationForm,
    'building-selector': BuildingSelector
  }
}
</script>
