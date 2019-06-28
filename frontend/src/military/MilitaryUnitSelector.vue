<template>
  <div>
    <div v-if="isSummon">
      N/A
    </div>
    <div v-else>
      <div class="slide-container">
        <input
          v-model="sliderValue"
          class="slider"
          :class="{ 'slider-disabled': isDisabled }"
          type="range"
          :name="army.key"
          min="0"
          :max="sliderSize"
          step="1"
          :style="{ width: sliderWidth + 'em' }"
          :hidden="cantTrain"
        >
      </div>
      <div v-if="isMonster">
        <span
          v-if="cantTrain"
          class="negative"
        >
          Requires more<br>{{ building.name }}
        </span>
        <tool-tip
          :content="sliderValue + ' of ' + army.maxTrainable"
          :tip="'Build more ' + building.name"
          align="left"
        />
      </div>
      <span
        v-else
        class="display"
        :hidden="cantTrain"
      >
        {{ sliderValue }}
      </span>
    </div>
  </div>
</template>

<script>
import ToolTip from '@/components/ToolTip.vue'

export default {
  name: 'MilitaryUnitSelector',
  components: {
    ToolTip,
  },
  props: {
    army: Object,
    building: Object,
    isMonster: Boolean,
    isSummon: Boolean,
    sliderSize: Number,
    value: Number,
  },
  data () {
    return {
      sliderValue: this.value,
    }
  },
  computed: {
    cantTrain () {
      return this.army.maxTrainable == 0
    },
    sliderWidth () {
      return Math.min(this.sliderSize + 0.8, 10)
    },
    isDisabled () {
      return this.sliderSize == 0
    },
  },
  watch: {
    sliderValue (val) {
      this.$emit('input', val)
    },
    value (val) {
      this.sliderValue = val
    }
  },
}
</script>

<style scoped>
.slide-container {
  display: flex;
  justify-content: space-around;
  width: 10em;
}

/* The slider itself */
.slider {
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
.slider::-webkit-slider-thumb {
  -webkit-appearance: none; /* Override default look */
  appearance: none;
  width: 0.4em; /* Set a specific slider handle width */
  height: 1.5em; /* Slider handle height */
  background: #4CAF50; /* Green background */
  cursor: pointer; /* Cursor on hover */
}

.slider::-moz-range-thumb {
  width: 0.4em; /* Set a specific slider handle width */
  height: 1.5em; /* Slider handle height */
  background: #4CAF50; /* Green background */
  cursor: pointer; /* Cursor on hover */
}

.slider-disabled::-moz-range-thumb  {
  background: grey;
}

.slider-disabled::-webkit-slider-thumb {
  background: grey;
}

@media (min-width: 640px) {

}
</style>
