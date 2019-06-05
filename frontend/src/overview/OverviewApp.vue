<template>
  <div
    id="content"
    class="invisible"
  >
    <prefix-title title="Overview" />
    <county-description />
    <div class="max-width-1 width-100-percent inner-content ">
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
      <h2
        id="news"
        class="tab-1 max-width-1"
      >
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
  mounted () {
    this.$hydrate('/api/overview/news')
    .then(() => {
      this.$el.classList.remove('invisible')
    })
  }
}
</script>

<style scoped>
#toggleNews {
  float: right;
  font-weight: normal;
  min-width: auto;
  width: 8em;
  height: auto;
}

@media (max-width: 640px) {
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
}

@media (min-width: 640px) {
  #content {
    margin: 1em 1em 0;
    flex-grow: 2;
  }

  h1 {
    padding-bottom: 0.8em;
    text-align: center;
  }

  .inner-content {
    max-width: initial;
  }

  h2 {
    padding-left: 1em;
    margin-bottom: 0.3em;
  }

  ul {
    margin-bottom: 1em;
  }

  #toggleNews {
    margin-top: 0.6em;
    height: 1.6em;
  }

  #news {
    height: 2.3em;
  }
}
</style>
