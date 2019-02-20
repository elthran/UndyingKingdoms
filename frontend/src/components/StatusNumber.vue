<template>
  <span :class="number < 0 ?'negative':'positive'">
    {{ fancyNum }}
  </span>
</template>

<script>
export default {
  name: 'StatusNumber',
  props: {
    'number': Number,
    'value': Number
  },
  computed: {
    fancyNum () {
      return (this.number <= 0 ? '\u00a0':'+\u00a0') + this.number
    }
  }
}
</script>
