<template>
  <div id="content">
    <prefix-title title="Overview" />
    <county-description />
    <div class="max-width-1 width-100-percent">
      <h2>Basics:</h2>
    </div>
    <overview-basics />
    <!-- <h2>Treasury:</h2>
    <ul>
      <li>
        Coffers: {{ county.gold }} <img
          class="resource_icons"
          src="/static/dist/images/gold_icon.jpg"
        >
      </li>
      <li>
        Lumber: {{ county.wood }} <img
          class="resource_icons"
          src="/static/dist/images/wood_icon.jpg"
        >
      </li>
      <li>
        Iron: {{ county.iron }} <img
          class="resource_icons"
          src="/static/dist/images/iron_icon.jpg"
        >
      </li>
      <li>
        Stone: {{ county.stone }} <img
          class="resource_icons"
          src="/static/dist/images/stone_icon.jpg"
        >
      </li>
      <li>
        Mana: {{ county.mana }} <img
          class="resource_icons"
          src="/static/dist/images/mana_icon.jpg"
        >
      </li>
    </ul>
    <h2>Citizens:</h2>
    <ul>
      <li>
        Population: {{ county.population }} <img
          class="resource_icons"
          src="/static/dist/images/population_icon.jpg"
        >
      </li>
      <li>
        Happiness: {{ county.happiness_terminology.title() }} <img
          class="resource_icons"
          src="/static/dist/images/happiness_icon.jpg"
        >
      </li>
      <li>
        Healthiness: {{ county.healthiness_terminology.title() }} <img
          class="resource_icons"
          src="/static/dist/images/healthiness_icon.jpg"
        >
      </li>
      <li>
        Stored Grain: {{ county.grain_stores }} <img
          class="resource_icons"
          src="/static/dist/images/grain_icon.jpg"
        >
      </li>
    </ul>
    <br>
    <p
      v-if="county.day < 1"
      id="serverMessageToPlayers"
      class="negative"
    />
    <h2>News</h2>
    Need to create a news array for display, so I can check it for empty
    <ul v-if="news.length">
      <li
        v-for="event in county.display_news() | sort(attribute='day', reverse=True)"
        :key="event.id"
      >
        Day: {{ event.day }} - {{ event.title }}: {{ event.content }}
      </li>
    </ul>
    <p v-else>
      No new events to report.
    </p>
    <br><br>
    <button onclick="oldNewsDisplay()">
      Show Old News
    </button>
    <div
      id="oldNews"
      class="invisible"
    >
      <br>
      <ul v-if="oldNews.length">
        <li
          v-for="event in county.display_old_news()|sort(attribute='day', reverse=True)"
          :key="event.id"
        >
          Day: {{ event.day }} - {{ event.title }}: {{ event.content }}
        </li>
      </ul>
      <p>There is no news in your history.</p>
    </div> -->
  </div>
</template>

<script>
import OverviewBasics from './OverviewBasics.vue'
import CountyDescription from './CountyDescription.vue'

export default {
  name: 'OverviewApp',
  components: {
    'overview-basics': OverviewBasics,
    'county-description': CountyDescription
  },
  data () {
    return {
      county: {
        kingdom: {
          world: Object
        },
        weather: {
          title: ''
        },
        happiness_terminology: {
          title: ''
        },
        healthiness_terminology: Object
      },
      news: Object,
      oldNews: Object
    }
  },
  beforeCreate () {
  }
}
</script>

<style scoped>
#content {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin: 1em;
}

h1 {
  padding-bottom: 0.4em;
  text-align: center;
}

h2 {
  padding-bottom: 0.3em;
}

button {
  width: 100%;
  height: 2.3em;
  border-radius: 4px;
}
</style>
