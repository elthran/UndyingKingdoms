<template lang="pug">
  #infrastructure-app.invisible
    prefix-title(title="City Planner")
    resource-header(
      @loaded="updateProgress"
    )
    idle-population-form.bottom-spacer-dot-6(
      @loaded="updateProgress"
    )
    building-selector.bottom-spacer-1(
      v-model="totalCosts"
      @loaded="updateProgress"
    )
    current-resources(
      :current-costs="totalCosts"
    )
</template>

<script>
import ResourceHeader from './ResourceHeader.vue'
import IdlePopulationForm from './IdlePopulationForm.vue'
import BuildingSelector from './BuildingSelector.vue'
import CurrentResources from './CurrentResources.vue'

export default {
  name: 'InfrastructureApp',
  components: {
    ResourceHeader,
    IdlePopulationForm,
    BuildingSelector,
    CurrentResources,
  },
  data () {
    return {
      totalCosts: {
        goldCost: 0,
        woodCost: 0,
        stoneCost: 0,
        landCost: 0,
        workersEmployed: 0
      },
      loadProgress: -3
    }
  },
  watch: {
    loadProgress (newVal) {
      if (newVal === 0) {
        this.$el.classList.remove('invisible')
      }
    }
  },
  methods: {
    updateProgress () {
      this.loadProgress += 1
    }
  },
}
</script>

<style scoped>
#infrastructure-app {
  margin: 1em 1em 0.6em;
}
</style>
