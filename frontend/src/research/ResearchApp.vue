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
    <!-- <form id="research-form" action="{{ url_for('research_api') }}" accept-charset="UTF-8">
      {{ form.csrf_token }}
      <p>Name:
        <select-generator
          v-model="selectedResearch"
          :options="{{ form.technology.choices | vuesafe }}"
          id-name="{{ form.technology.id }}"
        ></select-generator>
      </p>
      <p>Description: v{ description }</p>
      <p>Progress: v{ progressCurrent } / v{ progressRequired }</p>
    </form>
    <br><br>
    <h2>Known Technologies</h2>
    <ul>
      {% for technology in known_technologies %}
      <li>{{ technology.name.title() }}: {{ technology.description }}</li>
      {% else %}
        <li>No technologies have been researched yet.</li>
      {% endfor %}
    </ul><br><br><br>
    <h2>All Technologies (still in testing): When all techs of a tier are researched, the next tier is unlocked</h2>
    {% for technology in all_technologies %}
      <li>{{ technology.name.title() }} (Tier {{ technology.tier }}): {{ technology.description }}</li>
      {% endfor %} -->
  </div>
</template>

<script>
export default {
  name: 'ResearchApp',
  data () {
    return {
      county: Object,
      form: Object,
      urlFor: Object,
      researchChange: -1,
      selectedResearch: -1,
      description: '',
      progressCurrent: -1,
      progressRequired: -1,
    }
  },
  watch: {
    selectedResearch () {
      sendForm($('#research-form'), this.updatePage)
    }
  },
  mounted () {
    this.$hydrate('/api/research/data')
  },
  methods: {
    updatePage (data) {
      this.researchChange = data.researchChange;
      this.description = data.description;
      this.progressCurrent = data.progressCurrent;
      this.progressRequired = data.progressRequired;
    }
  }
}
// // Beautiful Jinja hacked in variables.
// var RESEARCH_CHANGE = {{ research_change }};
// var SELECTED_RESEARCH = {{ current_tech.id }};
// var DESCRIPTION = "{{ current_tech.description }}";
// var PROGRESS_CURRENT = {{ current_tech.current }};
// var PROGRESS_REQUIRED = {{ current_tech.cost }};
// // But please keep them separate.
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
