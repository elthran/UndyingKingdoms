<template>
  <select
    :id="idName"
    :name="idName"
    :value="value"
    @input="$emit('input', $event.target.value)"
  >
    <option
      v-for="option in options"
      :key="option[0]"
      :option="option"
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
    value: Number,
    idName: String
  }
}
</script>
