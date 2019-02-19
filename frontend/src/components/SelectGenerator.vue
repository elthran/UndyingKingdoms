<template>
  <select
    :id="idName"
    :name="idName"
    :value="value"
    @input="$emit('input', $event.target.value)"
  >
    <option
      v-for="option in options"
      :key="option.id"
      :selected="option[0] == selected"
      :value="option[0]"
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
    selected: [Number, String]
  },
  data () {
    return {
      key: [Number, String]
    }
  }
}
</script>
