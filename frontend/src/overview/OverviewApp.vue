<template>
  <div id="content">
    <prefix-title title="Overview" />
    <county-description />
    <div class="max-width-1 width-100-percent">
      <h2 class="tab-1">
        Basics
      </h2>
      <overview-basics />
      <h2 class="top-spacer-dot-6 tab-1">
        Treasury
      </h2>
      <overview-treasury />
      <h2 class="top-spacer-dot-6 tab-1">
        Citizens
      </h2>
      <overview-citizens />
      <br>
      <!-- <p
        v-if="county.day < 1"
        id="serverMessageToPlayers"
        class="negative"
      /> -->
      <h2 class="tab-1">
        News
        <button
          id="toggleNews"
          @click="newsVisibility = !newsVisibility"
        >
          {{ newsVisibility?'hide':'show' }} old news
        </button>
      </h2>
      <overview-news
        v-show="!newsVisibility"
        :news="news"
      />
      <overview-news
        v-show="newsVisibility"
        :news="oldNews"
      />
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

#toggleNews {
  float: right;
  font-weight: normal;
  min-width: auto;
  width: 7em;
  height: auto;
}
</style>
