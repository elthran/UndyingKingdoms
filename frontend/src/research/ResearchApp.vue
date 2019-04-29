<template>
  <div id="research-app">
    <h2>
      You currently gain {{ researchChange }} <img
        class="resource_icons"
        src="/static/dist/images/research_icon.jpg"
      > each day<span
        v-if="county.research > 0"
      > and you have {{ county.research }} bonus research</span>.
    </h2>
    <br>

    <h2>Current Research:</h2>
    <p>Note: More technologies become available as you complete all research within a tier.</p>
    <form
      id="research-form"
      ref="form"
      action="/api/research/update"
      accept-charset="UTF-8"
    >
      <div v-html="form.csrf_token.html" />
      <p>
        Name: <select-generator
          v-model="selectedResearch"
          :options="form.technology.choices"
          :id-name="form.technology.id"
        />
      </p>
      <p>Description: {{ description }}</p>
      <p>Progress: {{ progressCurrent }} / {{ progressRequired }}</p>
    </form>
    <br><br>
    <h2>Known Technologies</h2>
    <ul v-if="knownTechnologies.length > 0">
      <li
        v-for="technology in knownTechnologies"
        :key="technology.id"
      >
        {{ technology.name }}: {{ technology.description }}
      </li>
    </ul>
    <p v-else>
      No technologies have been researched yet.
    </p>
    <br><br><br>
    <h2>All Technologies (still in testing): When all techs of a tier are researched, the next tier is unlocked</h2>
    <ul>
      <li
        v-for="technology in allTechnologies"
        :key="technology.id"
      >
        {{ technology.name }} (Tier {{ technology.tier }}): {{ technology.description }}
      </li>
    </ul>
  </div>
</template>

<script>
import SelectGenerator from '@/components/SelectGenerator.vue'

export default {
  name: 'ResearchApp',
  components: {
    SelectGenerator,
  },
  data () {
    return {
      county: Object,
      form: {
        technology: {
          choices: [],
          id: '',
        },
        csrf_token: {
          html: '',
        }
      },
      urlFor: Object,
      researchChange: -1,
      selectedResearch: -1,
      description: '',
      progressCurrent: -1,
      progressRequired: -1,
      knownTechnologies: [],
      allTechnologies: [],
    }
  },
  watch: {
    selectedResearch () {

    }
  },
  mounted () {
    this.$hydrate('/api/research/update')
    .then(() => {
      this.$watch('selectedResearch', this.updatePage)
    })
  },
  methods: {
    updatePage (data) {
      console.log('selectedResearch changed')
      this.$sendForm(this.$refs.form)
      .then((data) => {
        console.log('selectedResearch should have saved')
        this.$deployData(data)
      }).catch((error) => {
        console.log(error.debugMessage)
      })
      // this.researchChange = data.researchChange;
      // this.description = data.description;
      // this.progressCurrent = data.progressCurrent;
      // this.progressRequired = data.progressRequired;
    }
  }
}
</script>

<style scoped>
@media (max-width: 640px) {
  #content {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin: 1em;
  }

  h2 {
      text-align: left;
      width: 280px;
      margin: auto;
      padding: 1.4em 0;
  }

  .form-control {
      width: 100%;
      margin-bottom: 4px;
  }

  button {
      width: 100%;
  }

  #spacer {
      height: 1.3em;
  }

  #checkboxDiv {
      width: 100%;
      text-align: left;
      max-width: 240px;
      margin-top: 0.6em;
  }
}
</style>
