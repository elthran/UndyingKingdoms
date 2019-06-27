<template>
  <div
    id="military-app"
    class="invisible"
  >
    <prefix-title title="War" />
    <div id="content">
      <military-strength
        v-if="ready"
        :county="county"
      />
      <military-form
        v-if="ready"
        :form="form"
        :metadata="metadata"
        :county="county"
        :armies="armies"
        :army-ordering="armyOrdering"
      />
      <br><br>
      <military-expeditions />
      <br style="margin-bottom: 2em">
    </div>
  </div>
</template>

<script>
import MilitaryStrength from './MilitaryStrength.vue'
import MilitaryForm from './MilitaryForm.vue'
import MilitaryExpeditions from './MilitaryExpeditions.vue'

export default {
  name: 'MilitaryApp',
  components: {
    MilitaryStrength,
    MilitaryForm,
    MilitaryExpeditions,
  },
  data () {
    return {
      loaded: false,
      county: null,
      form: null,
      metadata: null,
      armies: null,
      armyOrdering: null,
      ready: false,
    }
  },
  mounted () {
    this.$hydrate('/api/military/update')
    .then(() => {
      this.$el.classList.remove('invisible')
      this.ready = true
    })
  },
  methods: {
    updatePage () {
      return this.$hydrate('/api/military/update')
    }
  },
}
</script>

<style scoped>
@media (min-width: 640px) {
  #content {
    padding-top: 1em;
  }
}
</style>
