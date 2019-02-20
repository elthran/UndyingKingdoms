<template>
  <!-- This entire thing could be a component ... a generic one. -->
  <tr>
    <td>Iron</td>
    <td>{{ iron }}</td>
    <td>
      <status-number :number="ironIncome" />
      <img
        class="resource_icons"
        src="/static/dist/images/iron_icon.jpg"
      >
    </td>
    <td>-</td>
    <td>
      <ul>
        <li>
          {{ mines }}: {{ '+\u00a0' + ironIncome }} <img
            class="resource_icons"
            src="/static/dist/images/iron_icon.jpg"
          >
        </li>
      </ul>
    </td>
    <td>-</td>
    <td>Iron is used to equip powerful soldiers.</td>
  </tr>
</template>

<script>
import StatusNumber from '@/components/StatusNumber.vue'

export default {
  name: 'EconomyIronRow',
  components: {
    'status-number': StatusNumber
  },
  data () {
    return {
      iron: -1,
      ironIncome: -1,
      mines: ""
    }
  },
  beforeCreate () {
    this.$getData('/api/economy/iron', this.$deployData)
  }
}
</script>
