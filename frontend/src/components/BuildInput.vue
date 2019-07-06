<template lang="pug">
  div
    div.unit-input(
      v-if="isSummon"
    ) -
    input.unit-input(
      v-else
      v-model.number="safeValue"
      type="number"
      :name="army.key"
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
    army: Object,
    isSummon: Boolean,
    maxSize: Number,
    hideBottom: Boolean,
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
