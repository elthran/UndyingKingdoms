<template>
  <span :style="{ color: number < 0 ?'red':'green' }">
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

<style scoped>
.green {
    color: green;
}

.red {
    color: red;
}
</style>
