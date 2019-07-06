<template lang="pug">
  div
    div.unit-input(
      v-if="isSummon"
    ) -
    input.unit-input(
      v-else
      v-model.number="currentValue"
      type="number"
      min="0"
      :max="maxSize"
      :class="{ hideBottomBorder: hideBottom }"
      :disabled="isDisabled"
      @click.stop
    )
</template>

<!-- <div v-if="isSummon">
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
      :hidden="cantTrain && isMonster"
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
      :content="monsterCount + ' of ' + building.total"
      :tip="'Build more ' + building.name"
      align="left"
      class="top-spacer-dot-6"
    />
  </div>
  <span
    v-else
    class="display"
    :hidden="cantTrain"
  >
    {{ sliderValue }}
  </span>
</div> -->

<script>
import ToolTip from '@/components/ToolTip.vue'

export default {
  name: 'BuildInput',
  components: {
    ToolTip,
  },
  // model: {
  //   prop: 'value',
  //   event: 'input',
  // },
  props: {
    army: Object,
    building: Object,
    isMonster: Boolean,
    isSummon: Boolean,
    maxSize: Number,
    hideBottom: Boolean,
    value: Number,
  },
  data () {
    return {
      currentValue: this.value,
    }
  },
  computed: {
    cantTrain () {
      return this.army.maxTrainable == 0
    },
    isDisabled () {
      return this.maxSize == 0
    },
    monsterCount () {
      return this.army.available + this.army.currentlyTraining + this.currentValue
    },
  },
  watch: {
    currentValue (val) {
      this.$emit('input', Math.min(val, this.maxSize))
    },
    value (val) {
      this.currentValue = val
    }
  },
}
</script>

<style scoped>
.unit-input {
  padding: 0.3em;
  width: 3.3em;
  border-top: none;
  border-right: none;
}

.hideBottomBorder {
  border-bottom: none;
}
</style>
