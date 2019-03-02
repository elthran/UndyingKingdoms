<style>
#header {
    width: 310px;
    margin: auto;
}

h2 {
    margin: 0 1em 0.3em;
}

.tab {
    margin-left: 0.5em;
}
</style>

<template>
  <div id="header">
    <h2>Available Land: {{ availableLand }}&nbsp;/&nbsp;{{ land }}</h2>
    <h2>Citizens Available: {{ availableCitizens }}&nbsp;/&nbsp;{{ population }}</h2>
    <h2>
      Current Resources:
      <br>
      <span class="tab">
        {{ gold }} <img
          class="resource_icons"
          src="/static/dist/images/gold_icon.jpg"
        >
        {{ wood }} <img
          class="resource_icons"
          src="/static/dist/images/wood_icon.jpg"
        >
        {{ iron }} <img
          class="resource_icons"
          src="/static/dist/images/iron_icon.jpg"
        >
      </span>
      <!-- above from mobile version of site, below from desktop version-->
      <div class="top-spacer-1">
        Gold Cost: <span id="goldCost">0</span>
        <img
          class="resource_icons"
          src="/static/dist/images/gold_icon.jpg"
        > / {{ gold }} 
        <img
          class="resource_icons"
          src="/static/dist/images/gold_icon.jpg"
        >
      </div>
      <div>
        Wood Cost: <span id="woodCost">0</span>
        <img
          class="resource_icons"
          src="/static/dist/images/wood_icon.jpg"
        > / {{ wood }} 
        <img
          class="resource_icons"
          src="/static/dist/images/wood_icon.jpg"
        >
      </div>
      <div>
        Stone Cost: <span id="stoneCost">0</span>
        <img
          class="resource_icons"
          src="/static/dist/images/stone_icon.jpg"
        > / {{ stone }}
        <img
          class="resource_icons"
          src="/static/dist/images/stone_icon.jpg"
        >
      </div>
      <div class="top-spacer-dot-3">
        Land Required: <span id="landCost">0</span> / {{ availableLand }}
      </div>
      <br>
      <p>Each day, up to {{ buildSlots }} buildings in your queue will be built.</p>
      <br>
    </h2>
  </div>
</template>

<script>
export default {
  name: "ResourceHeader",
  data () {
    return {
      availableLand: -1,
      availableCitizens: -1,
      land: -1,
      population: -1,
      iron: -1,
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