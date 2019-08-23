<template lang="pug">
  div#body(
    :value="totalCosts"
    @input="$emit('input', computeTotalCosts())"
  )
    building-panel(
      v-for="buildingName in buildOrder"
      :key="buildingName"
      :building="buildings[buildingName]"
      v-model="resources"
    )
    button(
      id="submit-button"
      ref="submitButton"
      class="top-spacer-dot-6 width-100-percent"
      @click="submitForm"
    )
      | Build
    div.top-spacer-1
      | Total Buildings: {{ totalBuilt }}
    div Total Under Construction: {{ totalPending }}
    div Total Workers Employed: {{ totalEmployed }}
</template>

<script>
import BuildingPanel from './BuildingPanel'

export default {
  name: 'BuildingsManager',
  components: {
    BuildingPanel,
  },
  props: {
    totalCosts: Object
  },
  data () {
    return {
      buildOrder: ["house"],
      buildings: {
        "house": {
          name: "Cottage",
          total: -1,
          buildChoices: [0],  // can't use -1 here as it is an invalid Array length.
          amount: 0
        }
      },
      resources: {
        gold: 0, // this.county.gold,
        wood: 0, // this.county.wood,
        iron: 0, // this.county.iron,
        workers: 0, // this.county.availableWorkers,
      },
      totalBuilt: -1,
      totalEmployed: -1,
      totalPending: -1,
      formData: Object,
    }
  },
  mounted () {
    this.$hydrate('/api/infrastructure/buildings')
    .then(() => {
      this.$emit('loaded')
    })
  },
  methods: {
    submitForm () {
      this.amount = 0
      this.$refs.submitButton.disabled = true
      this.$sendData(this.buildFormData(), () => {
        this.$hydrate('/api/infrastructure/buildings')
      })
      setTimeout(() => {
        this.$refs.submitButton.disabled = false
      }, 2000)
    },
    computeTotalCosts () {
      var costs = {
        goldCost: 0,
        woodCost: 0,
        stoneCost: 0,
        landCost: 0,
        workersEmployed: 0
      }

      var count;
      var building;
      this.$nextTick(() => {  // fixes bug where computation is one selection delayed.
        for (var prop in this.buildings) {
          if (this.buildings.hasOwnProperty(prop)) {
            building = this.buildings[prop]
            count = building.amount
            costs.goldCost += building.goldCost * count
            costs.woodCost += building.woodCost * count
            costs.stoneCost += building.stoneCost * count
            costs.landCost += 1 * count  // currently all land costs are 1.
            costs.workersEmployed += building.workersEmployed * count
          }
        }
      })
      return costs
    },
    buildFormData () {
      for (var prop in this.buildings) {
        if (this.buildings.hasOwnProperty(prop)) {
          this.formData[prop] = this.buildings[prop].amount
          this.buildings[prop].amount = 0
        }
      }
      this.$emit('input', {  // reset all costs to 0.
        goldCost: 0,
        woodCost: 0,
        stoneCost: 0,
        landCost: 0,
        workersEmployed: 0
      })
      return this.formData
    },
  }
}
</script>

<style scoped>
@media (max-width: 640px) {
  #body {
      max-width: 19em;
      margin: auto;
  }

  #submit-button {
    margin-left: auto;
    margin-right: auto;
    position: sticky;
    bottom: 0.2em;
    left: 0;
    right: 0;
    z-index: 100;
  }
}

@media (min-width: 640px) {
  .top-bottom-padder-dot-6 {
    padding-top: 0.6em;
    padding-bottom: 0.6em;
  }
}
</style>
