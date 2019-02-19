<template>
  <tr>
    <td>
      Population
    </td>
    <td>{{ population }}</td>
    <!-- {% set population_projection = county.get_population_change(prediction=True) %}
    {% if population_projection >= 0 %}
    <td style="color:green;">+
    {% else %}
    <td style="color:red;">
    {% endif %}
    {{ population_projection }} <img class="resource_icons" src="/static/images/population_icon.jpg">
    </td>
    <td>
      <ul>
        {% if birth_rate_modifier.get(county.race)[1] %}
        <li>
        <div class="tooltip">{{ birth_rate_modifier.get(county.race)[0] }}: {{
        (birth_rate_modifier.get(county.race)[1] * 100)|int }}%<span class="tooltipText">Racial Modifier: {{ county.race }}</span>
        </div>
        </li>
        {% endif %}
        {% if birth_rate_modifier.get(county.background)[1] %}
        <li>({{ county.background }}) {{ birth_rate_modifier.get(county.background)[0] }}: {{
        (birth_rate_modifier.get(county.background)[1] * 100)|int }}%
        </li>
        {% endif %}
      </ul>
    </td>
    <td>
      <ul>
        <li>Births: {{ county.get_birth_rate() }}</li>
        <li>Immigration: {{ county.get_immigration_rate() }}</li>
      </ul>
    </td>
    <td>
      <ul>
        <li>Deaths: {{ county.get_death_rate() }}</li>
        <li>Emigration: {{ county.get_emigration_rate() }}</li>
      </ul>
    </td> -->
    <td>Raise happiness to lower the amount of emigrants leaving your county.</td>
  </tr>
</template>

<script>
import StatusNumber from '@/components/StatusNumber.vue'

export default {
  name: 'EconomyPopulationRow',
  components: {
    'status-number': StatusNumber
  },
  data () {
    return {
      population: Number,
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
      console.log(data);
      this.population = data.population
    }
  }
}
</script>
