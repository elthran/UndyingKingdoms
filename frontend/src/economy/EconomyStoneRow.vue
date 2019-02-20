<template>
  <economy-simple-row 
    title="Stone" 
    resourceName="stone"
    :descriptiveName="descriptiveName"
    description="Stone is used to build your most powerful buildings."
    :amount="stoneAmount"
    :income="stoneIncome"
  />
</template>

<!-- 
  <tr>
    <td>Stone</td>
    <td>{{ county.stone }}</td>
    {% if county.get_stone_income() >= 0 %}
    <td style="color:green;">
      +
      {% else %}
    </td><td style="color:red;">
      {% endif %}
      {{ county.get_stone_income() }} <img
        class="resource_icons"
        src="/static/images/stone_icon.jpg"
      >
    </td>
    <td>-</td>
    <td>
      <li>
        {{ county.buildings['quarry'].class_name_plural.title() }}: + {{ county.get_stone_income() }} <img
          class="resource_icons"
          src="/static/images/stone_icon.jpg"
        >
      </li>
    </td>
    <td>-</td>
    <td>Stone is used to build your most powerful buildings.</td>
  </tr> -->

<script>
import EconomySimpleRow from './EconomySimpleRow.vue'

export default {
  name: 'EconomyStoneRow',
  components: {
    'economy-simple-row': EconomySimpleRow
  },
  data () {
    return {
      stoneAmount: -1,
      stoneIncome: -1,
      descriptiveName: ""
    }
  },
  beforeCreate () {
    this.$getData('/api/economy/stone', this.$deployData)
  }
}
</script>
