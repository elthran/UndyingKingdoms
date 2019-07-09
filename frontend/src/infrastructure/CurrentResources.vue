<template lang="pug">
  #current-resouces
    h2.
      Current Resources:
    .tab
      | Gold Cost:&nbsp;
      status-text(
        :condition="currentCosts.goldCost <= gold"
        :text="currentCosts.goldCost"
      )
      resource-icon(type="gold")
      |  / {{ gold }}
      resource-icon(type="gold")
    .tab
      | Wood Cost:&nbsp;
      status-text(
        :condition="currentCosts.woodCost <= wood"
        :text="currentCosts.woodCost"
      )
      resource-icon(type="wood")
      |  / {{ wood }}
      resource-icon(type="wood")
    .tab
      | Stone Cost:&nbsp;
      status-text(
        :condition="currentCosts.stoneCost <= stone"
        :text="currentCosts.stoneCost"
      )
      resource-icon(type="stone")
      |  / {{ stone }}
      resource-icon(type="stone")
    //- .top-spacer-dot-3.tab
    //-   | Land Required:&nbsp;
    //-   status-text(
    //-     :condition="currentCosts.landCost <= availableLand"
    //-     :text="currentCosts.landCost"
    //-   ) / {{ availableLand }}
    br
    p.
      Each day, up to {{ buildSlots }} buildings in your queue will be built.
</template>

<script>
import ResourceIcon from '@/components/ResourceIcon.vue'
import StatusText from '@/components/StatusText.vue'

export default {
  components: {
    ResourceIcon,
    StatusText,
  },
  props: {
    currentCosts: {
      type: Object,
      default () {
        return {
          goldCost: -1,
          woodCost: -1,
          stoneCost: -1,
          landCost: -1,
          workersEmployed: -1
        }
      }
    }
  },
  data () {
    return {
      wood: -1,
      gold: -1,
      stone: -1,
      buildSlots: -1
    }
  },
  computed: {},
  methods: {},
}
</script>

<style scoped>
.tab {
  margin-left: 0.5em;
}

.sticky {
  position: sticky;
  top: 0.2em;
}
</style>
