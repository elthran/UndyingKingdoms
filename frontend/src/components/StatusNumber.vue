<template>
  <span :class="number < 0 ?'negative':'positive'">
    {{ (number <= 0 ? "&#160;":"+ ") + number }}
  </span>
</template>

<script>
export default {
  name: 'StatusNumber',
  props: {
    'number': Number,
    'value': Number
  }
}
</script>
