<style>
td:nth-child(2), td:nth-child(3) {
  text-align: center;
}
</style>

<template>
  <tr>
    <td>
      Population
    </td>
    <td>{{ county.population }}</td>
    <td>
      <status-number :number="county.population_projection"></status-number>
      <img class="resource_icons" src="/static/dist/images/population_icon.jpg">
    </td>
    <td>
      <ul v-if="county.birth_rate_mod">
        <li v-if="county.birth_rate_mod.race">
          <tool-tip
            :content="county.birth_rate_mod.race.name + ':\u00a0' + county.birth_rate_mod.race.value + '%'"
            :tip="'Racial Modifier: ' + county.race"
          ></tool-tip>
        </li>
        <li v-if="county.birth_rate_mod.background">
          ({{ county.background }}) {{ county.birth_rate_mod.background.name }}: {{ county.birth_rate_mod.background.value }}%
        </li>
      </ul>
    </td>
    <td>
      <ul>
        <li>Births: {{ county.birth_rate }}</li>
        <li>Immigration: {{ county.immigration_rate }}</li>
      </ul>
    </td>
    <td>
      <ul>
        <li>Deaths: {{ county.death_rate }}</li>
        <li>Emigration: {{ county.emigration_rate }}</li>
      </ul>
    </td>
    <td>Raise happiness to lower the amount of emigrants leaving your county.</td>
  </tr>
</template>

<script>
import StatusNumber from '@/components/StatusNumber.vue'
import ToolTip from '@/components/ToolTip.vue'

export default {
  name: 'countyPopulationRow',
  components: {
    'status-number': StatusNumber,
    'tool-tip': ToolTip
  },
  data () {
    return {
      county: Object,
      errors: Object
    }
  },
  beforeCreate () {
    this.axios.get('/api/economy/population')
      .then((response) => {
        if (response.data.status === 'success') {
          this.updatePage(response.data)
        } else {
          this.errors = response
        }
      })
      .catch((error) => {
        this.errors = error.response
      })
  },
  methods: {
    updatePage (data) {
      // console.log(data);
      this.county = data.county
    }
  }
}
</script>
