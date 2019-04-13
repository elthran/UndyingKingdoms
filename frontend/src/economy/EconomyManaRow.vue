<template>
  <economy-simple-row 
    title="Mana" 
    resource-name="mana"
    descriptive-name="Mana Flow"
    description="Mana is not yet implemented."
    :amount="manaAmount"
    :income="manaIncome"
  />
</template>

<script>
import EconomySimpleRow from './EconomySimpleRow.vue'

export default {
  name: 'EconomyManaRow',
  components: {
    'economy-simple-row': EconomySimpleRow
  },
  data () {
    return {
      manaAmount: -1,
      manaIncome: -1,
    }
  },
  mounted () {
    this.$hydrate('/api/economy/mana')
  }
}
</script>
