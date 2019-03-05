<style>
#header {
    max-width: 19em;
    margin: auto;
}

h2 {
    margin-bottom: 0.3em;
}

.tab {
    margin-left: 0.5em;
}
</style>

<template>
  <div id="header">
    <h2>Available Land: {{ availableLand }}&nbsp;/&nbsp;{{ land }}</h2>
    <h2>Citizens Available: {{ availableCitizens }}&nbsp;/&nbsp;{{ population }}</h2>
    <idle-population-form />
    <h2>
      Current Resources:
      <div class="tab">
        Gold Cost: {{ goldCost }}
        <img
          class="resource_icons"
          src="/static/dist/images/gold_icon.jpg"
        > / {{ gold }}
        <img
          class="resource_icons"
          src="/static/dist/images/gold_icon.jpg"
        >
      </div>
      <div class="tab">
        Wood Cost: {{ woodCost }}
        <img
          class="resource_icons"
          src="/static/dist/images/wood_icon.jpg"
        > / {{ wood }}
        <img
          class="resource_icons"
          src="/static/dist/images/wood_icon.jpg"
        >
      </div>
      <div class="tab">
        Stone Cost: {{ stoneCost }}
        <img
          class="resource_icons"
          src="/static/dist/images/stone_icon.jpg"
        > / {{ stone }}
        <img
          class="resource_icons"
          src="/static/dist/images/stone_icon.jpg"
        >
      </div>
      <div class="top-spacer-dot-3 tab">
        Land Required: {{ landCost }} / {{ availableLand }}
      </div>
      <br>
      <p>Each day, up to {{ buildSlots }} buildings in your queue will be built.</p>
      <br>
    </h2>
  </div>
</template>

<script>
import IdlePopulationForm from './IdlePopulationForm.vue'

export default {
  name: 'ResourceHeader',
  components: {
    'idle-population-form': IdlePopulationForm
  },
  data () {
    return {
      availableLand: -1,
      availableCitizens: -1,
      land: -1,
      population: -1,
      wood: -1,
      gold: -1,
      stone: -1,
      buildSlots: -1,
      stoneCost: 0,
      woodCost: 0,
      goldCost: 0,
      landCost: 0
    }
  },
  beforeCreate () {
    this.$getData('/api/infrastructure/resources', this.$deployData)
  }
}
</script>
