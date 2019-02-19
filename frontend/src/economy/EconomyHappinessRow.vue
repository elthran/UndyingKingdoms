<template>
  <tr>
    <td>Happiness</td>
    <td>{{ county.happiness }}%</td>
    <td>
      <status-number :number="happinessChange"></status-number>
      <img class="resource_icons" src="/static/images/heart_icon.jpg">
    </td>
    <td>-</td>
    <td>
      <ul>
        <li>Natural: +7 <img class="resource_icons" src="/static/images/heart_icon.jpg"></li>
        {% if county.production_choice == 3 %}
        <li>Relax: + {{ county.get_excess_production_value(3) }} <img class="resource_icons"
                                                                      src="/static/images/heart_icon.jpg">
        </li>
        {% endif %}
      </ul>
    </td>
    <td>
      <ul>
        {% if happiness_modifier.get(county.race)[0] %}
        <li>
          <div class="tooltip">{{ happiness_modifier.get(county.race)[0] }}: {{
            happiness_modifier.get(county.race)[1] }}<span class="tooltipText">Racial Modifier: {{ county.race }}</span>
          </div>
          <img class="resource_icons" src="/static/images/heart_icon.jpg">
        </li>
        {% endif %}
        <li>Taxes: v{ -selectedTaxRate } <img class="resource_icons" src="/static/images/heart_icon.jpg"></li>
      </ul>
    </td>
    <td>Happiness affects emigration rate and how productive your workers are. If they become too unhappy,
      they may start to question your rule.
    </td>
  </tr>
</template>

<script>
export default {
  name: 'EconomyHappinessRow'
}
</script>
