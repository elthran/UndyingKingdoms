<template>
  <div
    id="military-app"
    class="invisible"
  >
    <prefix-title title="War" />
    <div id="content">
      <military-strength
        :county="county"
      />
      <military-form
        :form="form"
        :metadata="metadata"
        :county="county"
      />
      <br><br>
      <!-- <military-expedtions /> -->
      <br style="margin-bottom: 2em">
    </div>
  </div>
</template>

<script>
import MilitaryStrength from './MilitaryStrength.vue'
import MilitaryForm from './MilitaryForm.vue'

export default {
  name: 'ResearchApp',
  components: {
    MilitaryStrength,
    MilitaryForm,
  },
  data () {
    return {
      loaded: false,
      county: null,
      form: null,
      metadata: null,
    }
  },
  mounted () {
    this.$hydrate('/api/military/update')
    .then(() => {
      this.$el.classList.remove('invisible')
    })
  },
  methods: {
    updatePage (data) {
      // this.$sendForm(this.$refs.form)
      // .then((data) => {
      //   this.$deployData(data)
      // }).catch((error) => {
      //   console.log(error.debugMessage)
      // })
    }
  }
}
</script>

<style scoped>
@media (min-width: 640px) {
  #content {
    padding-top: 1em;
  }
}
</style>
