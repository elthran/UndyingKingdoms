<template>
  <div
    id="research-app"
    class="invisible"
  >
    <prefix-title title="Scientist" />
    <h1 id="header">
      You currently gain {{ researchChange }} <img
        class="resource_icons"
        src="/static/dist/images/research_icon.jpg"
      > each day<span
        v-if="county.research > 0"
      > and you have {{ county.research }} bonus research</span>.
    </h1>
    <h2 class="bottom-spacer-dot-3">
      Current Research:
    </h2>
    <form
      id="research-form"
      ref="form"
      action="/api/research/update"
      accept-charset="UTF-8"
      class="tab-1"
    >
      <div v-html="form.csrf_token.html" />
      <div class="bottom-spacer-dot-3">
        Name: <select-generator
          v-model="selectedResearch"
          :options="form.technology.choices"
          :id-name="form.technology.id"
        />
      </div>
      <p>Description: {{ description }}</p>
      <p>Progress: {{ progressCurrent }} / {{ progressRequired }}</p>
      <p>More technologies will become available as you complete all research within a tier.</p>
    </form>
    <h2 class="top-spacer-dot-6 bottom-spacer-dot-3">
      Known Technologies
    </h2>
    <ul
      v-if="knownTechnologies.length > 0"
      class="tab-1"
    >
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
    <h2 class="top-spacer-dot-6 bottom-spacer-dot-3">
      All Technologies
    </h2>
    <p class="tab-2 bottom-spacer-dot-3">
      When all techs of a tier are researched, the next tier is unlocked
    </p>
    <ul class="tab-1">
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
      loaded: false,
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
  mounted () {
    this.$hydrate('/api/research/update')
    .then(() => {
      this.$watch('selectedResearch', this.updatePage)
      this.$el.classList.remove('invisible')
    })
  },
  methods: {
    updatePage (data) {
      this.$sendForm(this.$refs.form)
      .then((data) => {
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

@media (min-width: 640px) {
  #header {
    margin-top: 1.5em;
    margin-left: 1.5em;
    margin-bottom: 1.5em;
  }
}
</style>
