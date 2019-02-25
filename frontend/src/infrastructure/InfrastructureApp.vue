<template>
  <div id="infrastructure-app">
    <prefix-title title="City Planner" />
    <div id="layout-body">
      <nav-bar />
      <!-- <economy-form /> -->
    </div>
  </div>
</template>

<script>
import NavBar from '@/components/NavBar.vue'
// import EconomyForm from './EconomyForm.vue'

export default {
  name: 'InfrastructureApp',
  components: {
    'nav-bar': NavBar
    // 'economy-form': EconomyForm
  }
}
</script>

<style scoped>
#layout-body {
    display: flex;
    margin: 1em;
}
</style>
