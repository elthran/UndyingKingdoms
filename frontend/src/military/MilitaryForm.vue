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
        happiness: this.county.happiness,
      }
    }
  },
  computed: {
    happinessCost () {
      if (this.county.background == 'Warlord') {
        return 0
      } else {
        var sum = -999
        return Math.ceil(sum / this.county.population * 200)
      }
    },
    costs () {
      return {
        gold: this.county.gold - this.resources.gold,
        wood: this.county.wood - this.resources.wood,
        iron: this.county.iron - this.resources.iron,
        happiness: this.happinessCost,
      }
    }
  },
  mounted () {
  }
}
  // function updateCosts() {
  //     updateGold();
  //     updateWood();
  //     updateIron();
  //     updateHappiness();

  //     var gold = parseInt(goldCost.text());
  //     var wood = parseInt(woodCost.text());
  //     var iron = parseInt(ironCost.text());

  //     if (gold > totalGold) {
  //         goldCost.css("color", "red");
  //     } else {
  //         goldCost.css("color", "green");
  //     }

  //     if (wood > totalWood) {
  //         woodCost.css("color", "red");
  //     } else {
  //         woodCost.css("color", "green");
  //     }
  //     if (iron > totalIron) {
  //         ironCost.css("color", "red");
  //     } else {
  //         ironCost.css("color", "green");
  //     }
  //     if (gold <= totalGold && wood <= totalWood && iron <= totalIron) {
  //         submitButton.prop("disabled", false);
  //     } else {
  //         submitButton.prop("disabled", true);
  //     }

  //     resizeRemaining(gold, wood, iron);
  // }

  // sliders.each(function (index, element) {
  //     var size = parseInt($(element).prop("max"));
  //     if (size === 0) {
  //         $(element).addClass("slider-disabled");
  //     }
  //     $(element).css("width", calcSliderWidth(size));
  //     $(element).on("input", function () {
  //         displays[index].innerHTML = $(element).val();
  //         values[index].value = $(element).val();
  //         updateCosts();
  //     });
  // });
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
}
</style>
