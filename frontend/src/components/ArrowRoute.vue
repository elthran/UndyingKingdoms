<template>
  <span v-if="route.length < 2">
    {{ first.name }}
  </span>
  <span v-else>
    <a :href="first.url">{{ first.name }}</a> &#8594; <arrow-route :route="etc" />
  </span>
</template>

<script>
export default {
  name: 'ArrowRoute',
  props: {
    route: Array
  },
  computed: {
    first () {
      return this.route[0]
    },
    etc () {
      return this.route.slice(1)
    }
  }
}
</script>
