<template>
  <div>
    <div class="slide-container">
      <input
        class="slider"
        type="range"
        :name="army.key"
        value="0"
        min="0"
        :max="sliderSize"
        step="1"
        :hidden="cantTrain"
      >
    </div>
    <span
      class="display"
      :hidden="cantTrain"
    >
      0
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
  },
  computed: {
    cantTrain () {
      return this.army.maxTrainable == 0
    }
  }
}
</script>
