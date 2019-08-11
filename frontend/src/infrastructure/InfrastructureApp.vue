<template lang="pug">
  #infrastructure-app.invisible
    prefix-title(title="City Planner")
    resource-header(
      v-bind="infrastructure"
    )
    idle-population-form.bottom-spacer-dot-6(
      v-bind="infrastructure"
    )
    //- building-selector.bottom-spacer-1(
    //-   v-model="totalCosts"
    //-   @loaded="updateProgress"
    //- )
    //- current-resources(
    //-   :current-costs="totalCosts"
    //- )
</template>

<script>
import apiPaths from '@/assets/api-paths'
import http from '@/assets/http-helpers'

import ResourceHeader from './ResourceHeader.vue'
import IdlePopulationForm from './IdlePopulationForm.vue'
// import BuildingSelector from './BuildingSelector.vue'
// import CurrentResources from './CurrentResources.vue'

export default {
  name: 'InfrastructureApp',
  components: {
    ResourceHeader,
    IdlePopulationForm,
    // BuildingSelector,
    // CurrentResources,
  },
  data () {
    return {
      infrastructure: {},
      // totalCosts: {
      //   goldCost: 0,
      //   woodCost: 0,
      //   stoneCost: 0,
      //   landCost: 0,
      //   workersEmployed: 0
      // },
    }
  },
  watch: {
  },
  mounted () {
    http.get(apiPaths.infrastructure())
    .then((response) => {
      this.infrastructure = response.data
      this.show()
    })
  },
  methods: {
    show () {
      this.$el.classList.remove('invisible')
    }
  },
}
</script>

<style scoped>
#infrastructure-app {
  margin: 1em 1em 0.6em;
}
</style>
