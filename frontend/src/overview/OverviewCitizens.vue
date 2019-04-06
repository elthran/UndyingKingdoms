<template>
  <ul>
    <li>
      Population: {{ population }} <img
        class="resource_icons"
        src="/static/dist/images/population_icon.jpg"
      >
    </li>
    <li>
      Happiness: {{ happiness_term }} <img
        class="resource_icons"
        src="/static/dist/images/happiness_icon.jpg"
      >
    </li>
    <li>
      Healthiness: {{ healthiness_term }} <img
        class="resource_icons"
        src="/static/dist/images/healthiness_icon.jpg"
      >
    </li>
    <li>
      Stored Grain: {{ grain_stores }} <img
        class="resource_icons"
        src="/static/dist/images/grain_icon.jpg"
      >
    </li>
  </ul>
</template>

<script>
export default {
  name: 'OverviewCitizens',
  data () {
    return {
      population: -1,
      happiness_term: "someHappinessTerm",
      healthiness_term: "someHealthinessTerm",
      grain_stores: -1
    }
  },
  mounted () {
    this.$hydrate('/api/overview/citizens')
  }
}
</script>
