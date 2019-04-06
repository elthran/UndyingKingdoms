<template>
  <economy-simple-row 
    title="Stone" 
    resource-name="stone"
    :descriptive-name="descriptiveName"
    description="Stone is used to build your most powerful buildings."
    :amount="stoneAmount"
    :income="stoneIncome"
  />
</template>

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
  mounted () {
    this.$hydrate('/api/economy/stone')
  }
}
</script>
