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
      <!-- v-model="army.sliderSize" -->
      <military-army-row
        v-for="armyName in armyOrdering"
        :key="armyName"
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

    <!-- Maybe some kind of cost/resource component? -->
    <!-- <br>
    Gold Cost: <span id="goldCost">0</span>
    <img class="resource_icons" src="/static/images/gold_icon.jpg"> / {{ county.gold }} <img class="resource_icons" src="/static/images/gold_icon.jpg"><br>
    Wood Cost: <span id="woodCost">0</span>
    <img class="resource_icons" src="/static/images/wood_icon.jpg"> / {{ county.wood }} <img class="resource_icons" src="/static/images/wood_icon.jpg"><br>
    Iron Cost: <span id="ironCost">0</span>
    <img class="resource_icons" src="/static/images/iron_icon.jpg"> / {{ county.iron }} <img class="resource_icons"  src="/static/images/iron_icon.jpg"><br>
    Happiness Cost: <span id="happinessCost">0</span>
    <img class="resource_icons" src="/static/images/happiness_icon.jpg"> -->
    <br><br>
    <button
      id="submitButton"
      type="submit"
    >
      Build
    </button>
    <br>
    <!-- <div id="invisibleDataFields">
      <span id="population">{{ county.population }}</span>
      <span id="totalGold">{{ county.gold }}</span>
      <span id="totalWood">{{ county.wood }}</span>
      <span id="totalIron">{{ county.iron }}</span>
    </div> -->
  </form>
</template>

<script>
import MilitaryArmyRow from './MilitaryArmyRow.vue'

export default {
  name: 'MilitaryForm',
  components: {
    MilitaryArmyRow,
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
    }
  },
  mounted () {
    // for army in armies
    // army.sliderSize = calcBuildable(army)
  }
}
  // var sliders = $(".slider");
  // var displays = $(".display");
  // var values = $(".value");

  // var buildingGoldCosts = $(".buildingGoldCost");
  // var buildingWoodCosts = $(".buildingWoodCost");
  // var buildingIronCosts = $(".buildingIronCost");

  // var submitButton = $("#submitButton");
  // var goldCost = $("#goldCost");
  // var woodCost = $("#woodCost");
  // var ironCost = $("#ironCost");
  // var happinessCost = $("#happinessCost");


  // var totalGold = parseInt($("#totalGold").text());
  // var totalWood = parseInt($("#totalWood").text());
  // var totalIron = parseInt($("#totalIron").text());
  // var population = parseInt($("#population").text());

  // var monsterMax = parseInt($("#monsterMax").text());

  // function updateGold() {
  //     var sum = 0;
  //     sliders.each(function (index, element) {
  //         try {
  //           sum += element.value * buildingGoldCosts[index].innerHTML;
  //         }
  //         catch(err) {
  //         }
  //     });
  //     goldCost.html(sum);
  // }

  // function updateWood() {
  //     var sum = 0;
  //     sliders.each(function (index, element) {
  //         try {
  //           sum += element.value * buildingWoodCosts[index].innerHTML;
  //         }
  //         catch(err) {
  //         }
  //     });
  //     woodCost.html(sum);
  // }

  // function updateIron() {
  //     var sum = 0;
  //     sliders.each(function (index, element) {
  //         try {
  //           sum += element.value * buildingIronCosts[index].innerHTML;
  //         }
  //         catch(err) {
  //         }
  //     });
  //     ironCost.html(sum);
  // }

  // function updateHappiness() {
  //     var sum = 0;
  //     sliders.each(function (ignore, element) {
  //         sum += parseInt(element.value);
  //     });
  //     if ('{{ current_user.county.background }}' == 'Warlord') {
  //       happinessCost.html(0);
  //     } else {
  //       happinessCost.html(Math.ceil(sum / population * 200));
  //     }
  // }

  // function calcSliderWidth(size) {
  //     return Math.min(size + 0.8, 10) + "em";
  // }

  // function resizeRemaining(gold, wood, iron) {
  //     // console.log(sliders);
  //     sliders.each(function (index, element) {
  //         try {
  //           var goldPrice = buildingGoldCosts[index].innerHTML;
  //         }
  //         catch(err) {
  //           var goldPrice = 0;
  //         }
  //         try {
  //           var woodPrice = buildingWoodCosts[index].innerHTML;
  //         }
  //         catch(err) {
  //           var woodPrice = 0;
  //         }
  //         try {
  //           var ironPrice = buildingIronCosts[index].innerHTML;
  //         }
  //         catch(err) {
  //           var ironPrice = 0;
  //         }
  //         var isMonster = element.hasAttribute('data-monster');
  //         var currentSize = parseInt(element.value);
  //         var remaining = Math.max(Math.floor(Math.min(
  //             (totalGold - gold) / goldPrice,
  //             (totalWood - wood) / woodPrice,
  //             (totalIron - iron) / ironPrice,
  //             (isMonster) ? monsterMax-currentSize : Infinity
  //         )), 0);

  //         var size = currentSize + remaining;
  //         // need to include current element.value + current_max - remaining?
  //         $(element).prop("max", size);
  //         $(element).css("width", calcSliderWidth(size));
  //         if (size === 0) {
  //             $(element).addClass("slider-disabled");
  //         } else {
  //             $(element).removeClass("slider-disabled");
  //         }
  //     });
  //     // return remaining;
  // }

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
