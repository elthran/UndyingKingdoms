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
      <p class="bottom-spacer-dot-3">
        Description: {{ description }}
      </p>
      <p>Progress: {{ progressCurrent }} / {{ progressRequired }}</p>
      <p id="info">
        More technologies will become available after you complete their requirements.
      </p>
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
        {{ technology.name }} ({{ technology.source }}): {{ technology.description }}
      </li>
    </ul>
    <p v-else>
      No technologies have been researched yet.
    </p>
    <h2 class="top-spacer-dot-6 bottom-spacer-dot-3">
      Available Technologies
    </h2>
    <ul class="tab-1">
      <li
        v-for="tech in availableTechnologies"
        :key="tech.id"
      >
        {{ tech.name }} ({{ tech.source }}): {{ tech.description }} ({{ tech.current }} / {{ tech.cost }}
        <img
          class="resource_icons"
          src="/static/dist/images/research_icon.jpg"
        >)
      </li>
    </ul>
    <h2 class="top-spacer-dot-6 bottom-spacer-dot-3">
      Locked Technologies
    </h2>
    <ul class="tab-1">
      <li
        v-for="tech in lockedTechnologies"
        :key="tech.id"
      >
        {{ tech.name }} ({{ tech.source }}): {{ tech.description }} ({{ tech.current }} / {{ tech.cost }}
        <img
          class="resource_icons"
          src="/static/dist/images/research_icon.jpg"
        >)
      </li>
    </ul>
    <br style="margin-bottom: 2em">
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
      availableTechnologies: [],
      lockedTechnologies: [],
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
    }
  }
}
</script>

<style scoped>
#info {
  margin-top: 0.6em;
}

@media (max-width: 640px) {
  #research-app {
    margin: 1em 1em 0;
  }

  #header {
    margin-bottom: 0.6em;
  }

  #research-form {
    margin-left: 0;
  }

  h2 {
    text-align: center;
  }

  ul {
    margin-left: 0;
  }

  li {
    margin-bottom: 0.3em;
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
