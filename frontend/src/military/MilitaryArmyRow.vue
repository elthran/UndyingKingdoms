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
      <military-monster-selector
        v-if="isMonster"
        :army="army"
        :building="army.building"
        :slider-size="sliderSize"
        :slider-width="sliderWidth"
      />
      <div v-else-if="isSummon">
        N/A
      </div>
      <div v-else>
        <div class="slide-container">
          <input
            class="slider"
            type="range"
            :name="army.key"
            v-model="sliderValue"
            min="0"
            :max="sliderSize"
            step="1"
            :style="{ width: sliderWidth + 'em' }"
          >
        </div>
        <span class="display">{{ sliderValue }}</span>
      </div>
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
import MilitaryMonsterSelector from './MilitaryMonsterSelector.vue'

export default {
  name: 'MilitaryArmyRow',
  components: {
    MilitaryMonsterSelector
  },
  props: {
    army: Object,
    metadata: Object,
    county: Object,
  },
  data () {
    return {
      sliderValue: 0,
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
      var totalGold = this.county.gold
      var totalWood = this.county.wood
      var totalIron = this.county.iron

      var gold = this.county.goldRemaining || 0 // ?
      var wood = this.county.woodRemaining || 0 // ?
      var iron = this.county.ironRemaining || 0 // ?


      var goldPrice = this.army.gold || 0
      var woodPrice = this.army.wood || 0
      var ironPrice = this.army.iron || 0
      var currentSize = this.army.maxTrainable
      var remaining = Math.max(Math.floor(Math.min(
          (totalGold - gold) / goldPrice,
          (totalWood - wood) / woodPrice,
          (totalIron - iron) / ironPrice,
          (this.isMonster) ? this.army.maxTrainable - currentSize : Infinity
      )), 0)

      var size = currentSize + remaining
      return size
    },
    sliderWidth () {
      return Math.min(this.sliderSize + 0.8, 10)
    }
  },
  mounted () {
    // this.$set(this.army, sliderSize)
  },
}
</script>

<style scoped>
@media (min-width: 640px) {
  /deep/ .slide-container {
    display: flex;
    justify-content: space-around;
    width: 10em;
  }

  /* The slider itself */
  /deep/ .slider {
    -webkit-appearance: none;  /* Override default CSS styles */
    appearance: none;
    width: 100%; /* Full-width */
    height: 0.1em; /* Specified height */
    background: #d3d3d3; /* Grey background */
    outline: none; /* Remove outline */
    -webkit-transition: .2s; /* 0.2 seconds transition on hover */
    transition: opacity .2s;
    padding: 0.1em 0 0.1em;
    margin: 1em 0 1em;
    width: 10em;
  }

  /* The slider handle (use -webkit- (Chrome, Opera, Safari, Edge) and -moz- (Firefox) to override default look) */
  /deep/ .slider::-webkit-slider-thumb {
    -webkit-appearance: none; /* Override default look */
    appearance: none;
    width: 0.4em; /* Set a specific slider handle width */
    height: 1.5em; /* Slider handle height */
    background: #4CAF50; /* Green background */
    cursor: pointer; /* Cursor on hover */
  }

  /deep/ .slider::-moz-range-thumb {
    width: 0.4em; /* Set a specific slider handle width */
    height: 1.5em; /* Slider handle height */
    background: #4CAF50; /* Green background */
    cursor: pointer; /* Cursor on hover */
  }

  /deep/ .slider-disabled::-moz-range-thumb  {
    background: grey;
  }

  /deep/ .slider-disabled::-webkit-slider-thumb {
    background: grey;
  }
}
</style>
