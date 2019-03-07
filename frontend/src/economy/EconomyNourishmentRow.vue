<template>
  <tr>
    <td>Healthiness</td>
    <td>{{ healthiness }}%</td>
    <td>
      <status-number :number="healthinessChange" />
    </td>
    <td>-</td>
    <td>-</td>
    <td>-</td>
    <td>
      The better nourished your people, the healthier they will be.
      Your healthiness decreases by 1% for every 200 unfed people each day.
    </td>
  </tr>
</template>

<script>
import StatusNumber from '@/components/StatusNumber.vue'

export default {
  name: 'EconomyHealthinessRow',
  components: {
    'status-number': StatusNumber
  },
  props: {
    update: Boolean
  },
  data () {
    return {
      healthiness: -1,
      healthinessChange: -1
    }
  },
  watch: {
    update () {
      this.$getData('/api/economy/healthiness', this.$deployData)
    }
  },
  beforeCreate () {
    this.$getData('/api/economy/healthiness', this.$deployData)
  }
}
</script>
