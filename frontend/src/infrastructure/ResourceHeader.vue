<template>
  <div id="header">
    <h2>Available Land: {{ availableLand }}&nbsp;/&nbsp;{{ land }}</h2>
    <h2>Citizens Available: {{ availableCitizens }}&nbsp;/&nbsp;{{ population }}</h2>
    <!-- Slot allows me to inject the idle population allocation form here. -->
    <slot />
    <h2>Current Resources:</h2>
    <div class="tab">
      Gold Cost: {{ currentCosts.goldCost }}
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
      Wood Cost: {{ currentCosts.woodCost }}
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
      Stone Cost: {{ currentCosts.stoneCost }}
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
      Land Required: {{ currentCosts.landCost }} / {{ availableLand }}
    </div>
    <br>
    <p>Each day, up to {{ buildSlots }} buildings in your queue will be built.</p>
  </div>
</template>

<script>
export default {
  name: 'ResourceHeader',
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
      availableLand: -1,
      availableCitizens: -1,
      land: -1,
      population: -1,
      wood: -1,
      gold: -1,
      stone: -1,
      buildSlots: -1
    }
  },
  beforeCreate () {
    this.$getData('/api/infrastructure/resources', this.$deployData)
  }
}
</script>

<style scoped>
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
