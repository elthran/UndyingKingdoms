<template>
  <div>
    Gold Cost: {{ costs.gold }}
    <resource-icon type="gold" /> / {{ county.gold }} <resource-icon type="gold" /><br>
    Wood Cost: {{ costs.wood }}
    <resource-icon type="wood" /> / {{ county.wood }} <resource-icon type="wood" /><br>
    Iron Cost: {{ costs.iron }}
    <resource-icon type="iron" /> / {{ county.iron }} <resource-icon type="iron" /><br>
    Happiness Cost: {{ costs.happiness }}
    <resource-icon type="happiness" /> / {{ county.happiness }} <resource-icon type="happiness" />
    <div class="top-spacer-dot-3">
      Workers Cost: {{ costs.workers }} / {{ county.availableWorkers }}
    </div>
  </div>
</template>

<script>
import ResourceIcon from '@/components/ResourceIcon.vue'

export default {
  name: "MilitaryResources",
  components: {
    ResourceIcon,
  },
  props: {
    county: Object,
    costs: Object,
  },
  data () {
    return {

    }
  },
}
</script>
