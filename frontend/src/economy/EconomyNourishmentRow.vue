<template>
  <tr>
    <td>Nourishment</td>
    <td>{{ nourishment }}%</td>
    <td>
      <status-number :number="nourishmentChange" />
    </td>
    <td>-</td>
    <td>-</td>
    <td>-</td>
    <td>
      The better nourished your people, the healthier they will be.
      Your nourishment decreases by 1% for every 200 unfed people each day.
    </td>
  </tr>
</template>

<script>
import StatusNumber from '@/components/StatusNumber.vue'

export default {
  name: 'EconomyNourishmentRow',
  components: {
    'status-number': StatusNumber
  },
  data () {
    return {
      nourishment: -1,
      nourishmentChange: -1
    }
  },
  beforeCreate () {
    this.$getData('/api/economy/nourishment', this.$deployData)
  }
}
</script>
