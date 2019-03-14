<style scoped>
#body {
    max-width: 19em;
    margin: auto;
}

.tab {
  margin-left: 1em;
}
</style>

<template>
  <div id="body">
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
      <div>Cost: {{ currentBuilding.goldCost }}/{{ currentBuilding.woodCost }}/{{ currentBuilding.stoneCost }}</div>
      <div>Workers Employed: {{ currentBuilding.totalEmployed }} ({{ currentBuilding.workersEmployed }} each)</div>
      <div>Description: {{ currentBuilding.description }}</div>
    </div>
    <button
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
      this.$sendData(this.formData, () => {
        this.$getData('/api/infrastructure/buildings', this.$deployData)
      })
    }
  }
}
</script>
