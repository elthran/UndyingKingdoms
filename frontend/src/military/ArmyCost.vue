<template lang="pug">
  div.container
    | Cost:
    span
      div(v-if="isSummon") N/A
      span(v-else)
        span(v-if="costsGold")
          span(class="buildingGoldCost") {{ army.gold }}
          resource-icon(type="gold")
        span(v-if="costsWood")
          span(class="buildingWoodCost") {{ army.wood }}
          resource-icon(type="wood")
        span(v-if="costsIron")
          span(class="buildingIronCost") {{ army.iron }}
          resource-icon(type="iron")
        span(v-if="isFree")
          | Free
</template>

<script>
import ResourceIcon from '@/components/ResourceIcon.vue'

export default {
  name: 'ArmyCost',
  components: {
    ResourceIcon,
  },
  props: {
    army: Object,
    isSummon: Boolean,
  },
  data () {
    return {

    }
  },
  computed: {
    costsGold () {
      return this.army.gold > 0
    },
    costsIron () {
      return this.army.iron > 0
    },
    costsWood () {
      return this.army.wood > 0
    },
    isFree () {
      return (this.goldPrice + this.woodPrice + this.ironPrice) == 0
    },
  },
}
</script>

<style scoped>
.container {
  min-height: 2em;
}
</style>
