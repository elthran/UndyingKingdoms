<template>
  <select
    :id="idName"
    :name="idName"
    :value="value"
    :disabled="disabled"
    @input="$emit('input', $event.target.value)"
  >
    <option
      v-for="(option, index) in options"
      :key="index"
      :selected="option[0] == selected"
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
    value: [Number, String],
    idName: String,
    selected: [Number, String],
    disabled: Boolean,
    max: Number
  },
  data () {
    return {
    }
  }
}
</script>
