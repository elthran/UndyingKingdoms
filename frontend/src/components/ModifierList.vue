<template>
  <ul v-if="modifier">
    <li v-if="modifier.race">
      <tool-tip
        :content="raceContent"
        :tip="'Racial Modifier: ' + race"
      />
      <img
        v-if="img"
        class="resource_icons"
        :src="img"
      >
    </li>
    <li v-if="modifier.background">
      <tool-tip
        :content="backgroundContent"
        :tip="'Class Modifier: ' + background"
      />
      <img
        v-if="img"
        class="resource_icons"
        :src="img"
      >
    </li>
  </ul>
</template>

<script>
import ToolTip from './ToolTip.vue'

export default {
  name: "ModifierList",
  components: {
    'tool-tip': ToolTip
  },
  props: {
    modifier: [Object, Function],
    race: String,
    background: String,
    valueIcon: {
      type: String,
      default: '%'
    },
    img: String
  },
  computed: {
    raceContent () {
      return this.modifier.race.name + ':\u00a0' + this.modifier.race.value + this.valueIcon
    },
    backgroundContent () {
      return this.modifier.background.name + ':\u00a0' + this.modifier.background.value + this.valueIcon
    }
  }
}
</script>