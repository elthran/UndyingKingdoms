<template>
  <div id="economy-app">
    <prefix-title title="Economy"></prefix-title>
    <div id="layout-body">
      <side-bar></side-bar>
      <economy-form></economy-form>
    </div>
  </div>
</template>

<script>
import SideBar from "@/components/SideBar.vue"
import EconomyForm from "@/components/EconomyForm.vue"

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
