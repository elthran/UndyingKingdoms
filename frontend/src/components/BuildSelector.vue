<template lang="pug">
  div
</template>

<script>
import ToolTip from '@/components/ToolTip.vue'

export default {
  name: 'BuildSelector',
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
    monsterCount () {
      return this.army.available + this.army.currentlyTraining + this.sliderValue
    }
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
