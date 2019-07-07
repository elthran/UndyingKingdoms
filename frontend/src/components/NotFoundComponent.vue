<template>
  <div id="not-found-component">
    <p>404 - Page not found.</p>
    <br>
    Return to <a :href="/login/">login</a>
  </div>
</template>

<script>
export default {
  name: 'NotFoundComponent',
  mounted () {

  },
}
</script>

<style scoped>
#not-found-component {
  position: absolute;
  top: 33%;
  left: 50%;
  transform: translate(-50%, -50%);

  font-size: 1.5em;
  text-align: center;
}
</style>
