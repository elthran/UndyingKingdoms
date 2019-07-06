<template lang="pug">
  div
    div
      strong Unit Totals:
    div Available: {{ county.unitsAvailable }}
    div Training: {{ county.unitsInTraining }}
    div Traveling: {{ county.unitsUnavailable }}
    div
      | Cost:&nbsp;
      tool-tip(
        :content="county.upkeepCosts"
        :tip="metadata.upkeepDaily"
        align="right"
      )
</template>

<script>
import ToolTip from '@/components/ToolTip.vue'

export default {
  name: "MilitaryArmyTotals",
  components: {
    ToolTip,
  },
  props: {
    county: Object,
    metadata: Object,
  },
  data () {
    return {

    }
  }
}
</script>

<style scoped>
div {
  margin-bottom: 0.3em;
}
</style>
