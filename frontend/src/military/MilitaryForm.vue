<template>
  <form
    method="POST"
    accept-charset="UTF-8"
    role="form"
  >
    <span v-html="form.csrf_token.html" />
    <table>
      <tr>
        <th>Name</th>
        <th>Available</th>
        <th>Traveling</th>
        <th>Training</th>
        <th>Train</th>
        <th id="costCol">
          Cost
        </th>
        <th>
          <div class="tooltip">
            Attack<span class="tooltip-text">{{ metadata.attack }}</span>
          </div>
        </th>
        <th>
          <div class="tooltip">
            Defence<span class="tooltip-text">{{ metadata.defence }}</span>
          </div>
        </th>
        <th>
          <div class="tooltip">
            Health<span class="tooltip-text">{{ metadata.health }}</span>
          </div>
        </th>
        <th>Type</th>
        <th>Description</th>
      </tr>
      <military-army-row
        v-for="armyName in armyOrdering"
        :key="armyName"
        v-model="resources"
        :army="armies[armyName]"
        :metadata="metadata"
      />
      <tr class="total-row">
        <td>Total</td>
        <td>{{ county.unitsAvailable }}</td>
        <td>{{ county.unitsUnavailable }}</td>
        <td>{{ county.unitsInTraining }}</td>
        <td>-</td>
        <td>
          <div class="tooltip">
            {{ county.upkeepCosts }}<span
              class="tooltip-text"
            >{{ metadata.upkeepDaily }}</span>
          </div>
        </td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
      </tr>
    </table>
    <military-resources
      id="resources"
      :county="county"
      :costs="costs"
    />
    <button
      id="submitButton"
      type="submit"
    >
      Build
    </button>
    <br>
  </form>
</template>

<script>
import MilitaryArmyRow from './MilitaryArmyRow.vue'
import MilitaryResources from './MilitaryResources.vue'

export default {
  name: 'MilitaryForm',
  components: {
    MilitaryArmyRow,
    MilitaryResources,
  },
  props: {
    county: Object,
    form: Object,
    metadata: Object,
    armies: Object,
    armyOrdering: Array,
  },
  data () {
    return {
      resources: {
        gold: this.county.gold,
        wood: this.county.wood,
        iron: this.county.iron,
        workers: this.county.availableWorkers,
      }
    }
  },
  computed: {
    workerCosts () {
      return this.county.availableWorkers - this.resources.workers
    },
    happinessCost () {
      if (this.county.background == 'Warlord') {
        return 0
      } else {
        return Math.ceil(this.workerCosts / this.county.population * 200)
      }
    },
    costs () {
      return {
        gold: this.county.gold - this.resources.gold,
        wood: this.county.wood - this.resources.wood,
        iron: this.county.iron - this.resources.iron,
        workers: this.workerCosts,
        happiness: this.happinessCost,
      }
    }
  },
  mounted () {
  }
}
</script>

<style scoped>
@media (min-width: 640px) {
  input {
    padding: 0.5em 0 0;
  }

  #invisibleDataFields {
    display: none;
  }

  #costCol {
    min-width: 8.5em;
  }

  table {
    margin-top: 1em;
  }

  tr:nth-child(even) {background-color: #f2f2f2;}

  th, td {
    vertical-align: bottom;
    border: 1px solid #ddd;
    padding: 0 0.3em 0.3em;
  }

  th {
    font-weight: bold;
    vertical-align: middle;
  }

  .total-row {
    font-weight: bold;
    height: 2.6em;
  }

  .tooltip .tooltip-text {
    /* Position the tooltip */
    position: absolute;
    z-index: 1;
    top: 120%;
    left: 50%;
    margin-left: -195px; /* Use half of the width (120/2 = 60), to center the tooltip */
  }

  #resources {
    margin-top: 1em;
    margin-bottom: 1em;
  }
}
</style>
