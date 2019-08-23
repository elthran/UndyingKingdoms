<template lang="pug">
  div
    div.buildable-input(
      v-if="isSummon"
    ) -
    input.buildable-input(
      v-else
      v-model.number="safeValue"
      type="number"
      :name="buildable.key"
      :min="min"
      :max="maxSize"
      :class="{ hideBottomBorder: hideBottom }"
      :disabled="isDisabled"
      @click.stop
    )
</template>

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
    buildable: Object,
    isSummon: {
      type: Boolean,
      default () {
        return false
      }
    },
    hideBottom: Boolean,
    maxSize: Number,
    value: Number,
  },
  data () {
    return {
      currentValue: this.value,
      min: 0,
    }
  },
  computed: {
    isDisabled () {
      return this.maxSize == 0
    },
    safeValue: {
      get () {
        return this.currentValue
      },
      set (val) {
        this.currentValue = Math.max(
          Math.min(val, this.maxSize), this.min
        )
      },
    }
  },
  watch: {
    currentValue (val) {
      this.$emit('input', this.currentValue)
    },
    value (val) {
      this.currentValue = val
    }
  },
}
</script>

<style scoped>
.buildable-input {
  padding: 0.3em;
  width: 3.3em;
  border-top: none;
  border-right: none;
}

.hideBottomBorder {
  border-bottom: none;
}
</style>
