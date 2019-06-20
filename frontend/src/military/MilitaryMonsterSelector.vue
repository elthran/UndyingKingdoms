<template>
  <div>
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
        :hidden="cantTrain"
      >
    </div>
    <span
      class="display"
      :hidden="cantTrain"
    >
      {{ sliderValue }}
    </span>
    <span
      v-if="cantTrain"
      style="color:red;"
    >
      Requires more<br>{{ building.name }}
    </span>
    <span
      v-else
      class="tooltip"
    >of {{ army.maxTrainable }}
      <span class="tooltip-text">Build more {{ building.name }}</span>
    </span>
  </div>
</template>

<script>
export default {
  name: 'MilitaryMonsterSelector',
  props: {
    army: Object,
    building: Object,
    sliderSize: Number,
    sliderWidth: Number,
  },
  data () {
    return {
      sliderValue: 0,
    }
  },
  computed: {
    cantTrain () {
      return this.army.maxTrainable == 0
    }
  }
}
</script>
