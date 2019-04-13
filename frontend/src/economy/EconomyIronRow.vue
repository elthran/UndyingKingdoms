<template>
  <economy-simple-row 
    title="Iron" 
    resource-name="iron"
    :descriptive-name="mines"
    description="Iron is used to equip powerful soldiers."
    :amount="iron"
    :income="ironIncome"
  />
</template>

<script>
import EconomySimpleRow from './EconomySimpleRow.vue'

export default {
  name: 'EconomyIronRow',
  components: {
    'economy-simple-row': EconomySimpleRow
  },
  data () {
    return {
      iron: -1,
      ironIncome: -1,
      mines: ""
    }
  },
  mounted () {
    this.$hydrate('/api/economy/iron')
  }
}
</script>
