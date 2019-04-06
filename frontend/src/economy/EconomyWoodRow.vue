<template>
  <economy-simple-row 
    title="Lumber" 
    resource-name="wood"
    :descriptive-name="mills"
    description="Lumber is used to build buildings and to equip certain soldiers."
    :amount="wood"
    :income="woodIncome"
  />
</template>

<script>
import EconomySimpleRow from './EconomySimpleRow.vue'

export default {
  name: 'EconomyWoodRow',
  components: {
    'economy-simple-row': EconomySimpleRow
  },
  data () {
    return {
      wood: -1,
      woodIncome: -1,
      mills: "",
    }
  },
  mounted () {
    this.$hydrate('/api/economy/wood')
  }
}
</script>
