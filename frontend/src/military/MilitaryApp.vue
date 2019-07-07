<template lang="pug">
  div#military-app.invisible
    prefix-title(title="War")
    div
      military-strength(
        v-if="ready"
        :county="county"
      )
      br
      military-army-totals(
        v-if="ready"
        :county="county"
        :metadata="metadata"
      )
      military-form.bottom-spacer-2(
        v-if="ready"
        :form="form"
        :metadata="metadata"
        :county="county"
        :armies="armies"
        :army-ordering="armyOrdering"
      )
      military-expeditions#expeditions-spacer
    </div>
  </div>
</template>

<script>
import MilitaryStrength from './MilitaryStrength.vue'
import MilitaryForm from './MilitaryForm.vue'
import MilitaryExpeditions from './MilitaryExpeditions.vue'
import MilitaryArmyTotals from './MilitaryArmyTotals.vue'

export default {
  name: 'MilitaryApp',
  components: {
    MilitaryStrength,
    MilitaryForm,
    MilitaryExpeditions,
    MilitaryArmyTotals,
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
#military-app {
  padding-top: 1em;
  margin-right: 1em;
}

@media (max-width: 640px) {
  #military-app {
    margin-left: 1em;
  }

  #expeditions-spacer {
    margin-bottom: 1em;
  }
}

@media (min-width: 640px) {
  #military-app {
    width: 100%;
    max-width: 640px;
  }

  #expeditions-spacer {
    margin-bottom: 2em;
  }
}
</style>
