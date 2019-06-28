<style scoped>
#layout-content {
  width: 100%;
}

.tooltip .tooltip-text {
  /* Position the tooltip */
  position: absolute;
  z-index: 1;
  top: 120%;
  left: 50%;
  margin-left: -195px; /* Use half of the width (120/2 = 60), to center the tooltip */
}

#projected-growth-col {
  min-width: 10.1em;
}

#projected-losses-col {
  min-width: 9.5em;
}
</style>

<template>
  <div id="layout-content">
    <!--actual content -->
    <h1 class="center">
      Economy
    </h1>
    <form
      ref="form"
      action="/api/economy/update"
      accept-charset="UTF-8"
    >
      <span v-html="form.csrf_token.html" />
      <h2>Resources</h2>
      <table class="top-spacer-1">
        <tr class="grey-border">
          <th>Topic</th>
          <th>Current</th>
          <th>Projected Change</th>
          <th>Modifiers</th>
          <th id="projected-growth-col">
            Projected Growth
          </th>
          <th id="projected-losses-col">
            Projected Losses
          </th>
          <th>Notes</th>
        </tr>
        <economy-population-row />
        <economy-gold-row
          v-model="selectedTaxRate"
          :update="updateGold"
        />
        <economy-food-row
          v-model="selectedRations"
          :update="updateFood"
        />
        <economy-wood-row />
        <economy-iron-row />
        <economy-stone-row />
        <economy-mana-row />
        <economy-happiness-row
          :update="updateHappines"
        />
        <economy-nourishment-row
          :update="updateNourishment"
        />
        <economy-health-row />
      </table>
    </form>
  </div>
</template>

<script>
import EconomyPopulationRow from './EconomyPopulationRow.vue'
import EconomyGoldRow from './EconomyGoldRow.vue'
import EconomyFoodRow from './EconomyFoodRow.vue'
import EconomyWoodRow from './EconomyWoodRow.vue'
import EconomyIronRow from './EconomyIronRow.vue'
import EconomyStoneRow from './EconomyStoneRow.vue'
import EconomyManaRow from './EconomyManaRow.vue'
import EconomyHappinessRow from './EconomyHappinessRow.vue'
import EconomyNourishmentRow from './EconomyNourishmentRow.vue'
import EconomyHealthRow from './EconomyHealthRow.vue'

// The constants are defined at the beginning and use evil Jinja in JS.
export default {
  name: 'EconomyForm',
  components: {
    'economy-population-row': EconomyPopulationRow,
    'economy-gold-row': EconomyGoldRow,
    'economy-food-row': EconomyFoodRow,
    'economy-wood-row': EconomyWoodRow,
    'economy-iron-row': EconomyIronRow,
    'economy-stone-row': EconomyStoneRow,
    'economy-mana-row': EconomyManaRow,
    'economy-happiness-row': EconomyHappinessRow,
    'economy-nourishment-row': EconomyNourishmentRow,
    'economy-health-row': EconomyHealthRow
  },
  data () {
    return {
      form: {
        type: Object,
        csrf_token: Object
      },
      urlFor: Object,
      selectedTaxRate: Number,
      selectedRations: Number,
      updateGold: false,
      updateHappines: false,
      updateFood: false,
      updateNourishment: false,
      errors: Object
    }
  },
  watch: {
    selectedTaxRate () {
      this.$sendForm(this.$refs.form, () => {
        this.updateGold = !this.updateGold;
        this.updateHappines = !this.updateHappines;
      })
    },
    selectedRations () {
      this.$sendForm(this.$refs.form, () => {
        this.updateFood = !this.updateFood;
        this.updateNourishment = !this.updateNourishment;
      })
    }
  },
  mounted () {
    this.$hydrate('/api/economy/update')
  }
}
</script>
