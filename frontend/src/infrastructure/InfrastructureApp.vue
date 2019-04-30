<template>
  <div
    id="infrastructure-app"
    class="invisible"
  >
    <prefix-title title="City Planner" />
    <resource-header
      :current-costs="totalCosts"
      @loaded="loadProgress += 1"
    >
      <template v-slot:form>
        <idle-population-form
          @loaded="loadProgress += 1"
        />
        <div class="bottom-spacer-dot-6" />
      </template>
      <template v-slot:buildings>
        <building-selector
          v-model="totalCosts"
          @loaded="loadProgress += 1"
        />
      </template>
    </resource-header>
    <div class="bottom-spacer-1" />
  </div>
</template>

<script>
import ResourceHeader from './ResourceHeader.vue'
import IdlePopulationForm from './IdlePopulationForm.vue'
import BuildingSelector from './BuildingSelector.vue'

export default {
  name: 'InfrastructureApp',
  components: {
    ResourceHeader,
    IdlePopulationForm,
    BuildingSelector
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
}
</script>

<style scoped>
#infrastructure-app {
  margin: 1em 1em 0.6em;
}
</style>
