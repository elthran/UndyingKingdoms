<template>
  <tr>
    <td>Gold</td>
    <td>{{ county.gold }}</td>
    <td>
      <status-number :number="goldChange"></status-number>
      <img class="resource_icons" src="/static/images/gold_icon.jpg">
    </td>
    <td>
      <ul>
        <li>Tax Rate:
          <select-generator
            v-model="selectedTaxRate"
            :options="{{ form.tax.choices | vuesafe }}"
            id-name="{{ form.tax.id }}"
          ></select-generator>
          %
        </li>
        {% if income_modifier.get(county.race)[1] %}
        <li>
          <div class="tooltip">{{ income_modifier.get(county.race)[0] }}: {{
            (income_modifier.get(county.race)[1] * 100)|int }}%<span class="tooltipText">Racial Modifier: {{ county.race }}</span>
          </div>
        </li>
        {% endif %}
        {% if income_modifier.get(county.background)[1] %}
        <li>
          <div class="tooltip">{{ income_modifier.get(county.background)[0] }}: {{
            (income_modifier.get(county.background)[1] * 100)|int }}%<span class="tooltipText">Class Modifier: {{ county.background }}</span>
          </div>
        </li>
        {% endif %}
      </ul>
    </td>
    <td>
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
    </td>
    <!-- These conditions must not occur together or it will break the table. -->
    <td v-if="selectedTaxRate < 7" class="green">Your current tax rate has a positive effect on happiness</td>
    <td v-if="selectedTaxRate == 7">Your current tax rate has no effect on happiness</td>
    <td v-if="selectedTaxRate > 7" class="red">Your current tax rate has a negative effect on happiness</td>
  </tr>
</template>

<script>
export default {
  name: 'EconomyGoldRow'
}
</script>
