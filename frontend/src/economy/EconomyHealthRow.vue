<template>
  <tr>
    <td>Health</td>
    <td>
      <status-text 
        :condition="health >= 75"
        :text="healthTerminology"
      />
    </td>
    <td>
      <three-status-text 
        :number="healthChange"
      />
    </td>
    <td>-</td>
    <td>-</td>
    <td>-</td>
    <td>
      The current health of your people. If they become unhealthy, they will die at much greater rates and
      become very susceptible to disease and plague.
    </td>
  </tr>
</template>

<script>
import StatusText from '@/components/StatusText.vue'
import ThreeStatusText from '@/components/ThreeStatusText.vue'

export default {
  name: 'EconomyHealthRow',
  components: {
    'status-text': StatusText,
    'three-status-text': ThreeStatusText
  },
  data () {
    return {
      health: -1,
      healthChange: -1,
      healthTerminology: ""
    }
  },
  mounted () {
    this.$hydrate('/api/economy/health')
  }
}
</script>
