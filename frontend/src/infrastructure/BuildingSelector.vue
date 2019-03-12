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
    <form
      ref="build-form"
      :action="buildBuildingsUrl"
      accept-charset="UTF-8"
      @submit.prevent="submitForm"
    >
      <span v-html="form.csrf_token.html" />
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
        type="submit"
      >
        Build
      </button>
    </form>
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
      buildBuildingsUrl: String,
      form: {
        type: Object,
        csrf_token: Object
      },
      buildingsChoices: [
        ["house", "Cottage"]
      ],
      current: "house",
      buildings: {
        "house": {
          total: -1,
          buildChoices: [0]  // can't use -1 here as it is an invalid Array length.
        }
      },
      totalBuilt: -1,
      totalEmployed: -1,
      totalPending: -1,
      amount: 0,
      errors: Object
    }
  },
  computed: {
    currentBuilding () {
      return this.buildings[this.current]
    }
  },
  beforeCreate () {
    this.$getData('/api/infrastructure/buildings', this.$deployData)
  },
  methods: {
    submitForm () {
      this.$sendForm(this.$refs['build-form'], () => {
        console.log("form submitted")
        this.$getData('/api/infrastructure/buildings', this.$deployData)
      })
    }
  }
}
</script>
