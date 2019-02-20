<template>
  <ul v-if="modifier">
    <li v-if="modifier.race">
      <tool-tip
        :content="modifier.race.name + ':\u00a0' + modifier.race.value + '%'"
        :tip="'Racial Modifier: ' + race"
      />
    </li>
    <li v-if="modifier.background">
      <tool-tip
        :content="modifier.background.name + ':\u00a0' + modifier.background.value + '%'"
        :tip="'Class Modifier: ' + background"
      />
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
    background: String
  }
}
</script>