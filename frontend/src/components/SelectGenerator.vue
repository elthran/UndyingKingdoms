<template>
  <select
    :id="idName"
    v-model="selected"
    :name="idName"
    :disabled="disabled"
  >
    <option
      v-for="(option, index) in options"
      :key="index"
      :value="option[0]"
      :disabled="index > max"
    >
      {{ option[1] }}
    </option>
  </select>
</template>

<script>
export default {
  name: 'SelectGenerator',
  props: {
    options: Array,
    idName: String,
    disabled: Boolean,
    value: [Number, String],
    max: Number
  },
  data () {
    return {
      selected: null
    }
  },
  watch: {
    value (newValue) {
      this.selected = newValue
    },
    selected (newValue) {
      this.$emit('input', newValue)
    }
  }
}
</script>
