<template>
  <!-- [county.gold // army.gold, county.wood // army.wood, county.iron // army.iron]
        (list | sort)[0] replicates min()-->
  <!-- {% set slider_size = max_trainable_by_cost(county, army) %} -->
  <tr>
    <td>{{ army.name }}</td>
    <td>{{ army.available }}</td>
    <td>{{ army.traveling }}</td>
    <td>
      <div class="tooltip">
        {{ army.currentlyTraining }}
        <span class="tooltip-text">
          Max trainable per day: {{ army.trainablePerDay }}
        </span>
      </div>
    </td>
    <td>
      <military-unit-selector
        v-model="sliderValue"
        :army="army"
        :building="army.building"
        :slider-size="sliderSize"
        :is-monster="isMonster"
        :is-summon="isSummon"
      />
    </td>
    <td>
      <div v-if="isSummon">
        N/A
      </div>
      <div v-else>
        <span v-if="costsGold">
          <span class="buildingGoldCost">{{ army.gold }}</span><img
            class="resource_icons"
            src="/static/dist/images/gold_icon.jpg"
          >
        </span>
        <span v-if="costsWood">
          <span class="buildingWoodCost">{{ army.wood }}</span><img
            class="resource_icons"
            src="/static/dist/images/wood_icon.jpg"
          >
        </span>
        <span v-if="costsIron">
          <span class="buildingIronCost">{{ army.iron }}</span><img
            class="resource_icons"
            src="/static/dist/images/iron_icon.jpg"
          >
        </span>
        <span v-if="isFree">
          Free
        </span>
      </div>
    </td>
    <td>
      <div
        v-if="isBeseiger"
        class="tooltip"
      >
        *
        <span class="tooltip-text">
          {{ metadata.besiegerAttack }}
        </span>
      </div>
      <div v-else>
        {{ army.attack }}
      </div>
    </td>
    <td>{{ army.defence }}</td>
    <td>
      <div class="tooltip">
        {{ army.health }}
        <span class="tooltip-text">
          Armour type: {{ army.armourType }}
        </span>
      </div>
    </td>
    <td>{{ army.category }}</td>
    <td>{{ army.description }}</td>
  </tr>
</template>

<script>
import MilitaryUnitSelector from './MilitaryUnitSelector.vue'

export default {
  name: 'MilitaryArmyRow',
  components: {
    MilitaryUnitSelector
  },
  props: {
    army: Object,
    metadata: Object,
    value: Object,
  },
  data () {
    return {
      sliderValue: 0,
      resourcesRemaining: this.value,
    }
  },
  computed: {
    isMonster () {
      return this.army.key === 'monster'
    },
    isSummon () {
      return this.army.key === 'summon'
    },
    isBeseiger () {
      return this.army.key === 'besieger'
    },
    costsGold () {
      return this.army.gold > 0
    },
    costsIron () {
      return this.army.iron > 0
    },
    costsWood () {
      return this.army.wood > 0
    },
    isFree () {
      return this.army.gold == 0  && this.army.wood == 0 && this.army.iron == 0
    },
    sliderSize () {
      var goldPrice = this.army.gold * this.sliderValue || 0
      var woodPrice = this.army.wood * this.sliderValue || 0
      var ironPrice = this.army.iron * this.sliderValue || 0

      var totalGold = this.resourcesRemaining.gold - goldPrice
      var totalWood = this.resourcesRemaining.wood - woodPrice
      var totalIron = this.resourcesRemaining.iron - ironPrice

      var remaining = Math.max(Math.floor(Math.min(
          totalGold / goldPrice,
          totalWood / woodPrice,
          totalIron / ironPrice,
          this.army.maxTrainable - this.sliderValue
      )), 0)

      var size = this.sliderValue + remaining
      return size
    },
  },
  watch: {
    sliderValue (val, oldVal) {
      var resourcesRemaining = {
        gold: this.value.gold,
        wood: this.value.wood,
        iron: this.value.iron,
        workers: this.value.availableWorkers,
        happiness: this.value.happiness,
      }
      this.$emit('input', resourcesRemaining)
    }
  },
  mounted () {
    // this.$set(this.army, sliderSize)
  },
}
</script>

<style scoped>
@media (min-width: 640px) {
}
</style>
