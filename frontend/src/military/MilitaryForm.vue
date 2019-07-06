<template lang="pug">
  form(
    ref="form"
    method="POST"
    accept-charset="UTF-8"
    action="/api/military/update"
    @submit.prevent="updatePage"
  )
    span(v-html="form.csrf_token.html")
    military-army(
      v-for="armyName in armyOrdering"
      :key="armyName"
      v-model="resources"
      :army="armies[armyName]"
      :metadata="metadata"
      :reset="reset"
    )
    military-resources#resources(
      :county="county"
      :costs="costs"
    )
    button#submit-button(
      type="submit"
      :disabled="disabled"
    ) Train
    br
</template>

<script>
import MilitaryArmy from './MilitaryArmy.vue'
import MilitaryResources from './MilitaryResources.vue'

export default {
  name: 'MilitaryForm',
  components: {
    MilitaryArmy,
    MilitaryResources,
  },
  props: {
    county: Object,
    form: Object,
    metadata: Object,
    armies: Object,
    armyOrdering: Array,
  },
  data () {
    return {
      resources: {
        gold: this.county.gold,
        wood: this.county.wood,
        iron: this.county.iron,
        workers: this.county.availableWorkers,
      },
      reset: true,
      disabled: false,
    }
  },
  computed: {
    workerCosts () {
      return this.county.availableWorkers - this.resources.workers
    },
    happinessCost () {
      if (this.county.background == 'Warlord') {
        return 0
      } else {
        return Math.ceil(this.workerCosts / this.county.population * 200)
      }
    },
    costs () {
      return {
        gold: this.county.gold - this.resources.gold,
        wood: this.county.wood - this.resources.wood,
        iron: this.county.iron - this.resources.iron,
        workers: this.workerCosts,
        happiness: this.happinessCost,
      }
    }
  },
  methods: {
    updatePage (data) {
      this.disabled = true
      this.reset = !this.reset
      this.$sendForm(this.$refs.form)
      .then((data) => {
        this.disabled = false
        this.$parent.updatePage()
        .then(() => {
          this.resources = {
            gold: this.county.gold,
            wood: this.county.wood,
            iron: this.county.iron,
            workers: this.county.availableWorkers,
          }
        })
      }).catch((error) => {
        console.log(error.debugMessage)
      })
    }
  }
}
</script>

<style scoped>
#resources {
  margin-top: 1em;
  margin-bottom: 1em;
}

@media (max-width: 640px) {
  #submit-button {
    width: 100%;
  }
}

@media (min-width: 640px) {
}
</style>
