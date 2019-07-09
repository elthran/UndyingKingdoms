<template lang="pug">
  #resource-header
    h2.
      Available Land:
       {{ availableLand }}&nbsp;/&nbsp;{{ land }}
    h2.
      Citizens Available:
       {{ availableCitizens }}&nbsp;/&nbsp;{{ population }}
</template>

<script>
export default {
  name: 'ResourceHeader',
  components: {
  },
  props: {
  },
  data () {
    return {
      availableLand: -1,
      availableCitizens: -1,
      land: -1,
      population: -1,
    }
  },
  mounted () {
    this.$hydrate('/api/infrastructure/resources')
    .then(() => {
      this.$emit('loaded')
    })
  }
}
</script>

<style scoped>
#resource-header {
    max-width: 19em;
    margin: auto;
}

h2 {
    margin-bottom: 0.3em;
}
</style>
