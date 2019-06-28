<template>
  <img
    class="resource-icons"
    :src="src"
  >
</template>

<script>
export default {
  name: "ResourceIcon",
  props: {
    type: String,
  },
  computed: {
    src () {
      return "/static/dist/images/" + this.type + "_icon.jpg"
    }
  }
}
</script>

<style scoped>
.resource-icons {
  height: 1.25em;
  width: 1.25em;
}
</style>
