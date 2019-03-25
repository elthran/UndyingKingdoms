<template>
  <span :class="condition ? 'positive':'negative'">
    {{ text }}
  </span>
</template>

<script>
export default {
  name: 'StatusNumber',
  props: {
    'condition': Boolean,
    'text': [String, Number]
  }
}
</script>
