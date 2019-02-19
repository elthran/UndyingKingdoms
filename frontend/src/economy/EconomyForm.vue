<style scoped>
#layout-content {
  width: 100%;
}

.tooltip .tooltipText {
  /* Position the tooltip */
  position: absolute;
  z-index: 1;
  top: 120%;
  left: 50%;
  margin-left: -195px; /* Use half of the width (120/2 = 60), to center the tooltip */
}
</style>

<template>
  <div id="layout-content">
    <!--actual content -->
    <h1 class="center">
      Economy
    </h1>
    <form
      id="economy-form"
      :action="urlFor.update_economy"
      accept-charset="UTF-8"
    >
      {{ form.csrf_token }}
      <h2>Resources</h2>
      <table class="top-spacer-1">
        <tr class="grey-border">
          <th>Topic</th>
          <th>Current</th>
          <th>Projected Change</th>
          <th>Modifiers</th>
          <th>Projected Growth</th>
          <th>Projected Losses</th>
          <th>Notes</th>
        </tr>
        <economy-population-row></economy-population-row>
        <economy-gold-row></economy-gold-row>
        <!-- <economy-food-row></economy-food-row>
        <economy-wood-row></economy-wood-row>
        <economy-iron-row></economy-iron-row>
        <economy-stone-row></economy-stone-row>
        <economy-happiness-row></economy-happiness-row>
        <economy-nourishment-row></economy-nourishment-row>
        <economy-health-row></economy-health-row> -->
      </table>
    </form>
  </div>
</template>

<script>
import $ from 'jquery'
import EconomyPopulationRow from './EconomyPopulationRow.vue'
import EconomyGoldRow from './EconomyGoldRow.vue'
// import EconomyFoodRow from './EconomyFoodRow.vue'
// import EconomyWoodRow from './EconomyWoodRow.vue'
// import EconomyIronRow from './EconomyIronRow.vue'
// import EconomyStoneRow from './EconomyStoneRow.vue'
// import EconomyHappinessRow from './EconomyHappinessRow.vue'
// import EconomyNourishmentRow from './EconomyNourishmentRow.vue'
// import EconomyHealthRow from './EconomyHealthRow.vue'
// // ugly Jinja hacked in variables.
// var TAX = {{ county.tax }};
// var GOLD_CHANGE = {{ county.get_gold_change() }};
// var HAPPINESS_CHANGE = {{ county.get_happiness_change() }};
// var GRAIN_STORAGE_CHANGE = {{ county.grain_storage_change() }};
// var RATIONS = {{ county.rations }};
// var FOOD_EATEN = {{ county.get_food_to_be_eaten() }};
// var NOURISHMENT_CHANGE = {{ county.get_nourishment_change() }};
// // end of Jinja code. Please keep it inside here.

// The constants are defined at the beginning and use evil Jinja in JS.
export default {
  name: 'EconomyForm',
  components: {
    'economy-population-row': EconomyPopulationRow,
    'economy-gold-row': EconomyGoldRow,
    // 'economy-food-row': EconomyFoodRow,
    // 'economy-wood-row': EconomyWoodRow,
    // 'economy-iron-row': EconomyIronRow,
    // 'economy-stone-row': EconomyStoneRow,
    // 'economy-happiness-row': EconomyHappinessRow,
    // 'economy-nourishment-row': EconomyNourishmentRow,
    // 'economy-health-row': EconomyHealthRow
  },
  data () {
    return {
      form: Object,
      urlFor: Object,
      goldChange: Number,
      taxIncome: Number,
      selectedTaxRate: Number,
      happinessChange: Number,
      grainStorageChange: Number,
      selectedRations: Number,
      foodEaten: Number,
      nourishmentChange: Number,
      errors: Object
    }
  },
  watch: {
    selectedTaxRate () {
      this.sendForm($('#economy-form'), this.updatePage)
    },
    selectedRations () {
      this.sendForm($('#economy-form'), this.updatePage)
    }
  },
  beforeCreate () {
    // consider putting this in a general function?
    // this.axios.get('/api/economy')
    //   .then((response, status) => {
    //     if (status === 200) {
    //       this.updatePage(response.data)
    //     } else {
    //       this.errors = response
    //     }
    //   })
    //   .catch((error) => {
    //     this.errors = error.response
    //   })
  },
  methods: {
    updatePage (data) {
      this.form = data.form
      this.urlFor = data.urlFor
      this.goldChange = data.goldChange
      this.taxIncome = data.taxIncome
      this.happinessChange = data.happinessChange
      this.grainStorageChange = data.grainStorageChange
      this.foodEaten = data.foodEaten
      this.nourishmentChange = data.nourishmentChange
    },
    sendForm (form, callback) {
      $.ajax({
        url: form.attr('action'),
        method: 'POST',
        // need to verify csrf id, I might be wrong.
        headers: { 'X-CSRF-TOKEN': $('#csrf_token').val() },
        data: form.serialize(),
        dataType: 'json' // type of data returned, not type sent.
      })
        .always(function (data, status) {
          if (status === 'success') {
            callback(data)
          } else {
            this.errors = data
          }
        })
    }
  }
}
</script>
