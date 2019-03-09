<style scoped>
#body {
    max-width: 19em;
    margin: auto;
}
</style>

<template>
  <div id="body">
    <form
      ref="form"
      :action="urlFor.buildBuildings"
      accept-charset="UTF-8"
    >
      <span v-html="form.csrf_token.html" />
    </form>
    <select-generator
      v-model="current"
      :options="buildingsChoices"
      :selected="current"
      id-name="buildings"
    />
  </div>
</template>

<script>
import SelectGenerator from '@/components/SelectGenerator.vue'

export default {
  name: 'BuildingSelector',
  components: {
    'select-generator': SelectGenerator
  },
  data () {
    return {
      buildingsChoices: [Object],
      current: -1,
      urlFor: Object,
      form: {
        type: Object,
        csrf_token: Object
      }
    }
  },
  beforeCreate () {
    this.$getData('/api/infrastructure/buildings', this.$deployData)
  }
}
</script>
