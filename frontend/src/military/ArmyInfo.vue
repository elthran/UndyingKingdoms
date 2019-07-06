<template lang="pug">
  div
    div
      | Available: {{ army.available }}
    div
      | Training:&nbsp;
      tool-tip(
        :content="army.currentlyTraining"
        :tip="'Max trainable per day: ' + army.trainablePerDay"
        align="right"
      )
    div
      | Away: {{ army.traveling }}
    div
      tool-tip(
        content="Attack"
        :tip="metadata.attack"
        align="right"
        tip-width="10em"
      )
      | : {{ army.attack }}
    div
      tool-tip(
        content="Defence"
        :tip="metadata.defence"
        align="right"
      )
      | : {{ army.defence }}
    div
      tool-tip(
        content="Health"
        :tip="metadata.health"
        align="right"
      )
      | :&nbsp;
      tool-tip(
        :content="army.health"
        :tip="'Armour type: ' + army.armourType"
        align="right"
        tooltip-width="8em"
      )
    div Type: {{ army.category }}
    div Description: {{ army.description }}
    div.top-spacer-dot-3(
      v-if="hasAbility"
    ) Abilites:&nbsp;
      tool-tip(
        :content="army.ability"
        :tip="army.abilityDescription"
        align="top"
        tip-width="12em"
      )
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
  },
  computed: {
    hasAbility () {
      return this.army.ability != "None"
    },
  },
}
</script>
