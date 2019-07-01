<template lang="pug">
  div
    div
      | Available: {{ army.available }}
    div
      | Training:
      tool-tip(
        :content="army.currentlyTraining"
        :tip="'Max trainable per day: ' + army.trainablePerDay"
        align="right"
      )
    div
      | Away: {{ army.traveling }}
    div
      tool-tip(
        content="Attack:"
        :tip="metadata.attack"
        align="right"
        tip-width="10em"
      )
      |  {{ army.attack }}
    div Defence: {{ army.defence }}
    div Type: {{ army.category }}
    div Description: {{ army.description }}
</template>

<script>
import ToolTip from '@/components/ToolTip.vue'

export default {
  name: 'ArmyInfo',
  components: {
    ToolTip,
  },
  props: {
    army: Object,
    metadata: Object,
  },
  data () {
    return {

    }
  }
}
</script>
