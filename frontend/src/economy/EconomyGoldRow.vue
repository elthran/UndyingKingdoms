<template>
  <tr
    :value="tax"
    @input="$emit('input', $event.target.value)"
  >
    <td>Gold</td>
    <td>{{ gold }}</td>
    <td>
      <status-number :number="goldChange" />
      <img
        class="resource_icons"
        src="/static/dist/images/gold_icon.jpg"
      >
    </td>
    <td>
      Tax Rate:<br>
      <select-generator
        v-model="tax"
        :options="form.tax.choices"
        :selected="tax"
        :id-name="form.tax.id"
      />%
      <!-- Consider making this a component. -->
      <ul v-if="income_mod">
        <li v-if="income_mod.race">
          <tool-tip 
            :content="income_mod.race.name + ':\u00a0' + income_mod.race.value + '%'"
            :tip="'Racial Modifier: ' + race"
          />
        </li>
        <li v-if="income_mod.background">
          <tool-tip
            :content="income_mod.background.name + ':\u00a0' + income_mod.background.value + '%'"
            :tip="'Class Modifier' + background"
          />
        </li>
      </ul>
    </td>
    <!-- <td>
      <ul>
        <li>Taxes: v{ taxIncome }</li>
        {% if county.buildings['bank'].total > 0 %}
        <li>Banks: {{ county.get_bank_income() }}</li>
        {% endif %}
        {% if county.production_choice == 0 %}
        <li>Overworking: + {{ county.get_excess_production_value(0) }}</li>
        {% endif %}
      </ul>
    </td>
    <td>
      <ul>
        <li>Military Expenses: {{ county.get_upkeep_costs() }}</li>
      </ul>
    </td> -->
    <!-- These conditions must not occur together or it will break the table. -->
    <td
      v-if="tax < 7"
      class="green"
    >
      Your current tax rate has a positive effect on happiness
    </td>
    <td v-if="tax == 7">
      Your current tax rate has no effect on happiness
    </td>
    <td
      v-if="tax > 7"
      class="red"
    >
      Your current tax rate has a negative effect on happiness
    </td>
  </tr>
</template>

<script>
import SelectGenerator from '@/components/SelectGenerator.vue'
import StatusNumber from '@/components/StatusNumber.vue'
import ToolTip from '@/components/ToolTip.vue'

export default {
  name: 'EconomyGoldRow',
  components: {
    'status-number': StatusNumber,
    'select-generator': SelectGenerator,
    'tool-tip': ToolTip
  },
  data () {
    return {
      gold: 50,
      tax: 7,
      rations: 0,
      goldChange: 7,
      happinessChange: 7,
      grainStorageChange: 7,
      foodEaten: 7,
      nourishmentChange: 7,
      income_mod: Object,
      race: String,
      background: String,
      form: {
        tax: {
          choices: [Array],  // for some reason using default args this way fixes the linting bug.
          id: ""
        }
      },
      errors: Object
    }
  },
  beforeCreate () {
    this.$getData('/api/economy/gold', this.$deployData)   
  }
}
</script>
