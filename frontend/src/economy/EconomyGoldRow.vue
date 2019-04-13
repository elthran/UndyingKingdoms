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
      Tax Rate:
      <select-generator
        v-model="tax"
        :options="form.tax.choices"
        :selected="tax"
        :id-name="form.tax.id"
      />&nbsp;%
      <modifier-list 
        :modifier="income_mod"
        :race="race"
        :background="background"
      />
    </td>
    <td>
      <ul>
        <li>
          Taxes: {{ taxIncome }}
        </li>
        <li v-if="hasBanks">
          Banks: {{ bankIncome }}
        </li>
        <li v-if="isOverworking">
          Overworking: {{ '+\u00a0' + excessProduction }}
        </li>
      </ul>
    </td>
    <td>
      <ul>
        <li>
          Military Expenses: {{ militaryExpenses }}
        </li>
      </ul>
    </td>
    <td>
      <!-- These conditions must not occur together or it will break the table. -->
      <!-- Also note tha v-if, v-if-else, v-else doesn't seem to work. -->
      <p 
        v-if="tax < 7"
        class="positive"
      >
        Your current tax rate has a positive effect on happiness
      </p>
      <p v-else-if="tax == 7">
        Your current tax rate has no effect on happiness
      </p>
      <p
        v-else
        class="negative"
      >
        Your current tax rate has a negative effect on happiness
      </p>
    </td>
  </tr>
</template>

<script>
import SelectGenerator from '@/components/SelectGenerator.vue'
import StatusNumber from '@/components/StatusNumber.vue'
import ModifierList from '@/components/ModifierList.vue'

export default {
  name: 'EconomyGoldRow',
  components: {
    'status-number': StatusNumber,
    'select-generator': SelectGenerator,
    'modifier-list': ModifierList
  },
  props: {
    update: Boolean
  },
  data () {
    return {
      gold: -1,
      tax: -1,
      rations: -1,
      goldChange: -1,
      income_mod: Object,
      race: "",
      background: "",
      taxIncome: -1,
      bankIncome: -1,
      hasBanks: Boolean,
      isOverworking: Boolean,
      excessProduction: -1,
      militaryExpenses: -1,
      form: {
        tax: {
          choices: [Array],  // for some reason using default args this way fixes the linting bug.
          id: ""
        }
      },
      errors: Object
    }
  },
  watch: {
    update () {
      this.$hydrate('/api/economy/gold')
    }
  },
  mounted () {
    this.$hydrate('/api/economy/gold')
  }
}
</script>
