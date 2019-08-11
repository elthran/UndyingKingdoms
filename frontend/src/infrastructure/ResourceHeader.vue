<template lang="pug">
  #resource-header
    h2.
      Land Available:
       {{ landAvailable }}&nbsp;/&nbsp;{{ land }}
    h2.
      Citizens Available:
       {{ citizensAvailable }}&nbsp;/&nbsp;{{ citizens }}
    h2(
      :class="fullEfficiency ? 'positive' : 'negative'"
    ) Your buildings are currently {{ efficiencyAsPercent }}% efficient.
      div(
        v-if="!fullEfficiency"
      ) You need {{ citizensNeeded }} more citizens to fully utilize your infrastructure.
</template>

<script>
export default {
  name: 'ResourceHeader',
  components: {
  },
  props: {
    landAvailable: Number,
    citizensAvailable: Number,
    land: Number,
    citizens: Number,
    citizensNeeded: Number,
    efficiency: Number,
  },
  data () {
    return {}
  },
  computed: {
    fullEfficiency () {
      return this.citizensNeeded === 0
    },
    efficiencyAsPercent () {
      return Math.floor(this.efficiency * 100)
    }
  },
}
</script>

<style scoped>
@media(max-width: 640px) {
  #resource-header {
    max-width: 19em;
    margin: auto;
  }
}

h2 {
  margin-bottom: 0.3em;
}
</style>
