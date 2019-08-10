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
import apiPaths from '@/assets/api-paths'

export default {
  name: 'ResourceHeader',
  components: {
  },
  props: {
  },
  data () {
    return {
      landAvailable: -1,
      citizensAvailable: -1,
      land: -1,
      citizens: -1,
      citizensNeeded: -1,
      efficiency: -1,
    }
  },
  computed: {
    fullEfficiency () {
      return this.citizensNeeded === 0
    },
    efficiencyAsPercent () {
      return Math.floor(this.efficiency * 100)
    }
  },
  mounted () {
    this.$hydrate(apiPaths.infrastructure())
    .then(() => {
      this.$emit('loaded')
    })
  }
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
