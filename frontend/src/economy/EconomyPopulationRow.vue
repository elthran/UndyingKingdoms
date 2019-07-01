<style scoped>
td:nth-child(2), td:nth-child(3) {
  text-align: center;
}
</style>

<template>
  <tr>
    <td>
      Population
    </td>
    <td>{{ population }}</td>
    <td>
      <status-number :number="population_projection" />
      <img
        class="resource_icons"
        src="/static/dist/images/population_icon.jpg"
      >
    </td>
    <td>
      <modifier-list
        :modifier="birth_rate_mod"
        :race="race"
        :background="background"
      />
    </td>
    <td>
      <ul>
        <li>Births: {{ birth_rate }}</li>
        <li>Immigration: {{ immigration_rate }}</li>
      </ul>
    </td>
    <td>
      <ul>
        <li>Deaths: {{ death_rate }}</li>
        <li>Emigration: {{ emigration_rate }}</li>
      </ul>
    </td>
    <td>Raise happiness to lower the amount of emigrants leaving your county.</td>
  </tr>
</template>

<script>
import StatusNumber from '@/components/StatusNumber.vue'
import ModifierList from '@/components/ModifierList.vue'

export default {
  name: 'EconomyPopulationRow',
  components: {
    'status-number': StatusNumber,
    'modifier-list': ModifierList
  },
  data () {
    return {
      background: "",
      race: "",
      birth_rate: -1,
      birth_rate_mod: Object,
      death_rate: -1,
      emigration_rate: -1,
      immigration_rate: -1,
      population: -1,
      population_projection: -1,
      errors: Object
    }
  },
  mounted () {
    this.$hydrate('/api/economy/population')
  }
}
</script>
