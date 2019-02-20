<template>
  <tr>
    <td>Lumber</td>
    <td>{{ wood }}</td>
    <td>
      <status-number :number="woodIncome" />
      <img
        class="resource_icons"
        src="/static/dist/images/wood_icon.jpg"
      >
    </td>
    <td>-</td>
    <td>
      <ul>
        <li>
          {{ mills }}: {{'+\u00a0' + woodIncome }}
          <img
            class="resource_icons"
            src="/static/dist/images/wood_icon.jpg"
          >
        </li>
      </ul>
    </td>
    <td>-</td>
    <td>Lumber is used to build buildings and to equip certain soldiers.</td>
  </tr>
</template>

<script>
import StatusNumber from '@/components/StatusNumber.vue'

export default {
  name: 'EconomyWoodRow',
  components: {
    'status-number': StatusNumber
  },
  data () {
    return {
      wood: -1,
      woodIncome: -1,
      mills: "",
    }
  },
  beforeCreate () {
    this.$getData('/api/economy/wood', this.$deployData)
  }
}
</script>
