<template>
  <div
    id="body"
    :value="totalCosts"
    @input="$emit('input', computeTotalCosts())"
  >
    <div class="top-spacer-1">
      <div>
        Name:
        <select-generator
          v-model="current"
          :options="buildingsChoices"
          :selected="current"
          id-name="building"
        />
      </div>
      <div class="top-spacer-dot-6">
        To Be Built:
        <select-generator
          v-model="amount"
          :options="currentBuilding.buildChoices"
          selected="0"
          id-name="amount"
        />
      </div>
      <div class="top-spacer-dot-6">
        Owned: {{ currentBuilding.total }}
      </div>
      <div>Under Construction: {{ currentBuilding.pending }}</div>
      <div>
        Cost: {{ currentBuilding.goldCost }}
        <img
          class="resource_icons"
          src="/static/dist/images/gold_icon.jpg"
        >
        / {{ currentBuilding.woodCost }}
        <img
          class="resource_icons"
          src="/static/dist/images/wood_icon.jpg"
        >
        / {{ currentBuilding.stoneCost }}
        <img
          class="resource_icons"
          src="/static/dist/images/stone_icon.jpg"
        >
      </div>
      <div>Workers Employed: {{ currentBuilding.totalEmployed }} ({{ currentBuilding.workersEmployed }} each)</div>
      <div>Description: {{ currentBuilding.description }}</div>
    </div>
    <button
      ref="submitButton"
      class="top-spacer-dot-6 width-100-percent"
      @click="submitForm"
    >
      Build
    </button>
    <div class="top-spacer-1">
      Total Buildings: {{ totalBuilt }}
    </div>
    <div>Total Under Construction: {{ totalPending }}</div>
    <div>Total Workers Employed: {{ totalEmployed }}</div>
  </div>
</template>

<script>
import SelectGenerator from '@/components/SelectGenerator.vue'

export default {
  name: 'BuildingSelector',
  components: {
    'select-generator': SelectGenerator
  },
  props: {
    totalCosts: Object
  },
  data () {
    return {
      current: "house",
      amount: 0,
      buildingsChoices: [
        ["house", "Cottage"]
      ],
      buildings: {
        "house": {
          total: -1,
          buildChoices: [0]  // can't use -1 here as it is an invalid Array length.
        }
      },
      totalBuilt: -1,
      totalEmployed: -1,
      totalPending: -1,
      formData: Object,
      errors: Object
    }
  },
  computed: {
    currentBuilding () {
      return this.buildings[this.current]
    }
  },
  watch: {
    current (newVal, oldVal) {
      this.$nextTick(() => {  // fixes bug where amount defaults to 0
        this.amount = this.formData[newVal]
      })
    },
    amount (newVal) {
      this.formData[this.current] = newVal
    }
  },
  beforeCreate () {
    this.$getData('/api/infrastructure/buildings', this.$deployData)
  },
  methods: {
    submitForm () {
      this.amount = 0
      this.$refs.submitButton.disabled = true
      this.$sendData(this.formData, () => {
        this.$getData('/api/infrastructure/buildings', this.$deployData)
      })
      setTimeout(() => {
        this.$refs.submitButton.disabled = false
      }, 3000)
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
            count = this.formData[prop]
            building = this.buildings[prop]
            costs.goldCost += building.goldCost * count
            costs.woodCost += building.woodCost * count
            costs.stoneCost += building.stoneCost * count
            costs.landCost += 1 * count  // currently all land costs are 1.
            costs.workersEmployed += building.workersEmployed * count
          }
        }
      })
      return costs
    }
  }
}
</script>

<style scoped>
#body {
    max-width: 19em;
    margin: auto;
}

.tab {
  margin-left: 1em;
}
</style>
