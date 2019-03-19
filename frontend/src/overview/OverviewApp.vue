<template>
  <div id="content">
    <prefix-title title="Overview" />
    <county-description />
    <div class="max-width-1 width-100-percent">
      <h2>Basics:</h2>
      <overview-basics class="tab-1" />
      <h2 class="top-spacer-dot-6">
        Treasury:
      </h2>
      <overview-treasury class="tab-1" />
      <h2 class="top-spacer-dot-6">
        Citizens:
      </h2>
      <overview-citizens class="tab-1" />
      <br>
      <!-- <p
        v-if="county.day < 1"
        id="serverMessageToPlayers"
        class="negative"
      /> -->
      <h2>News</h2>
      <overview-news
        v-show="!newsVisibility"
        :news="news"
        class="tab-1"
      />
      <overview-news
        v-show="newsVisibility"
        :news="oldNews"
        class="tab-1"
      />
      <br>
      <button
        @click="newsVisibility = !newsVisibility"
      >
        Show Old News
      </button>
    </div>
  </div>
</template>

<script>
import OverviewBasics from './OverviewBasics.vue'
import CountyDescription from './CountyDescription.vue'
import OverviewTreasury from './OverviewTreasury.vue'
import OverviewCitizens from './OverviewCitizens.vue'
import OverviewNews from './OverviewNews.vue'

export default {
  name: 'OverviewApp',
  components: {
    'overview-basics': OverviewBasics,
    'county-description': CountyDescription,
    'overview-treasury': OverviewTreasury,
    'overview-citizens': OverviewCitizens,
    'overview-news': OverviewNews
  },
  data () {
    return {
      news: [],
      oldNews: [],
      newsVisibility: false
    }
  },
  beforeCreate () {
    this.$getData('/api/overview/news', this.$deployData)
  }
}
</script>

<style scoped>
#content {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin: 1em 1em 0;
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
