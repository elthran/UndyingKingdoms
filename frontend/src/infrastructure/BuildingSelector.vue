<template lang="pug">
  div#body(
    :value="totalCosts"
    @input="$emit('input', computeTotalCosts())"
  )
    //- using open by default during testing?
    collapsible(
      v-for="(key, index) in buildOrder"
      :key="index"
      :open="true"
      class="top-spacer-1 striped"
    )
      div
        | Name: {{ buildings[key].name }}
      div.top-spacer-dot-6
        | To Be Built:
        select-generator(
          v-model="buildings[key].amount"
          :options="buildings[key].buildChoices"
          selected="0"
          :id-name="'amount-' + key"
          :disabled="buildings[key].buildChoices.length===1"
          :max="buildings[key].max"
        )
        //- max is not yet implemented
      div.top-spacer-dot-6
        | Owned: {{ buildings[key].total }}
      div Under Construction: {{ buildings[key].pending }}
      div
        | Cost: {{ buildings[key].goldCost }}
        img(
          class="resource_icons"
          src="/static/dist/images/gold_icon.jpg"
        )
        | / {{ buildings[key].woodCost }}
        img(
          class="resource_icons"
          src="/static/dist/images/wood_icon.jpg"
        )
        | / {{ buildings[key].stoneCost }}
        img(
          class="resource_icons"
          src="/static/dist/images/stone_icon.jpg"
        )
      div Workers Employed: {{ buildings[key].totalEmployed }} ({{ buildings[key].workersEmployed }} each)
      div Description: {{ buildings[key].description }}
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
import Collapsible from '@/components/Collapsible'
import SelectGenerator from '@/components/SelectGenerator'

export default {
  name: 'BuildingSelector',
  components: {
    SelectGenerator,
    Collapsible,
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
      totalBuilt: -1,
      totalEmployed: -1,
      totalPending: -1,
      formData: Object,
      errors: Object
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
    }
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

.tab {
  margin-left: 1em;
}


.striped:nth-child(odd) {
  background-color: #f2f2f2;
  padding: 1em;
  border-radius: 1em;
}
</style>
