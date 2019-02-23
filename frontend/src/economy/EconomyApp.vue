<template>
  <div id="economy-app">
    <prefix-title title="Economist" />
    <div id="layout-body">
      <side-bar />
      <economy-form />
    </div>
  </div>
</template>

<script>
import SideBar from '@/components/SideBar.vue'
import EconomyForm from './EconomyForm.vue'

export default {
  name: 'EconomyApp',
  components: {
    'side-bar': SideBar,
    'economy-form': EconomyForm
  }
}
</script>

<style scoped>
#layout-body {
    display: flex;
    margin: 1em;
}
</style>
