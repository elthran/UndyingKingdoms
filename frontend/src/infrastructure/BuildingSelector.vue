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
      ref="form"
      :action="urlFor.buildBuildings"
      accept-charset="UTF-8"
    >
      <span v-html="form.csrf_token.html" />
    </form>
    <table>
      <tr>
        <td>Name</td>
        <td>To Be Built</td>
      </tr>
      <tr>
        <td>
          <select-generator
            v-model="current"
            :options="buildingsChoices"
            :selected="current"
            id-name="building"
          />
        </td>
        <td class="width-100-percent center">
          <select-generator
            :options="currentBuilding.buildChoices"
            selected="0"
            id-name="amount"
          />
        </td>
      </tr>
      <tr>
        <td colspan="2">
          <div class="top-spacer-dot-3">
            <div>Owned: {{ currentBuilding.total }}</div>
            <div>Under Construction: {{ currentBuilding.pending }}</div>
            <div>Cost: {{ currentBuilding.goldCost }}/{{ currentBuilding.woodCost }}/{{ currentBuilding.stoneCost }}</div>
            <div>Workers Employed: {{ currentBuilding.totalEmployed }} ({{ currentBuilding.workersEmployed }} each)</div>
            <div>Description: {{ currentBuilding.description }}</div>
          </div>
        </td>
      </tr>
    </table>
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
      urlFor: Object,
      form: {
        type: Object,
        csrf_token: Object
      },
      buildingsChoices: [
        [0, "Example"]
      ],
      current: 0,
      buildings: {
        "Example": {
          total: -1,
          buildChoices: [0]  // can't use -1 here as it is an invalid Array length.
        }
      },
      totalBuilt: -1,
      totalEmployed: -1,
      totalPending: -1
    }
  },
  computed: {
    name () {
      return this.buildingsChoices[this.current][1]
    },
    currentBuilding () {
      return this.buildings[this.name]
    }
  },
  beforeCreate () {
    this.$getData('/api/infrastructure/buildings', this.$deployData)
  }
}
</script>
