<template>
  <div id="app">
    <prefix-title title="Economy"></prefix-title>
    <div id="layout-body">
      <side-bar></side-bar>
      <economy-form></economy-form>
    </div>
  </div>
</template>

<script>
import SideBar from "@/components/SideBar.vue"
import StatusNumber from "@/components/StatusNumber.vue"
import SelectGenerator from "@/components/SelectGenerator.vue"
import EconomyForm from "@/components/EconomyForm.vue"

export default {
  name: 'app',
  components: {
    'side-bar': SideBar,
    'status-number': StatusNumber,
    'select-generator': SelectGenerator,
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
