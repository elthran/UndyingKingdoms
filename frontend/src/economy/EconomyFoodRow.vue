<template>
  <tr>
    <td>Food</td>
    <td>{{ county.grain_stores }}</td>
    <td>
      <status-number :number="grainStorageChange" />
      <img
        class="resource_icons"
        src="/static/images/grain_icon.jpg"
      >
    </td>
    <td>
      <ul>
        <li>
          Rations:
          <select-generator
            v-model="selectedRations"
            :options="{{ form.rations.choices | vuesafe }}"
            id-name="{{ form.rations.id }}"
          />
        </li>
        {% if food_consumed_modifier.get(county.race)[1] %}
        <li>
          <div class="tooltip">
            {{ food_consumed_modifier.get(county.race)[0] }}: {{
            (food_consumed_modifier.get(county.race)[1] * 100)| }}%<span class="tooltipText">
              Racial Modifier: {{ county.race }}
            </span>
          </div>
        </li>
        {% endif %}
      </ul>
    </td>
    <td>
      <ul>
        <li>
          Fields: + {{ county.get_produced_grain() }} <img
            class="resource_icons"
            src="/static/images/grain_icon.jpg"
          >
        </li>
        <li>
          Pastures: + {{ county.get_produced_dairy() }} <img
            class="resource_icons"
            src="/static/images/dairy_icon.jpg"
          >
        </li>
        {% if county.production_choice == 2 %}
        <li>
          Foraging: + {{ county.get_excess_production_value(2) }} <img
            class="resource_icons"
            src="/static/images/dairy_icon.jpg"
          >
        </li>
        {% endif %}
      </ul>
    </td>
    <td>
      <ul>
        <li>To be Eaten: v{ foodEaten }</li>
      </ul>
    </td>
    <td>
      Excess dairy can not be stored in your granaries. If you do not have enough food, your populace will
      begin to starve.
    </td>
  </tr>
</template>

<script>
export default {
  name: 'EconomyFoodRow'
}
</script>
