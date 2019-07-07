<template lang="pug">
  div#army-cost
    | Cost:&nbsp;
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
      return (this.army.gold + this.army.wood + this.army.iron) == 0
    },
  },
}
</script>

<style scoped>
#army-cost {
  min-height: 2em;
  display: flex;
  align-items: flex-end;
  margin-bottom: 0.6em;
}

/*#cost-col {
  min-width: 8.5em;
}*/
</style>
