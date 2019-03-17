<style scoped>
/* The main sidebar which is always visible when logged in */
.mobile-sidebar {
  display: flex;
  flex-direction: column;
  align-items: center;
  font-size: 1.5em;
  margin: 0 0 0.5em;
}

a {
  margin: 0.1em;
  padding: 0.1em;
  border: solid;
  border-width: 0.05em;
  border-color: gray;
  border-radius: 0.2em;
  text-decoration: none;
}

.bold {
  font-weight: bold;
}

.spacer {
  margin-bottom: 1em;
}

.flex-group {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
}
</style>

<template>
  <nav class="mobile-sidebar">
    <hr class="width-100-percent">
    <router-link :to="urlFor.overview">
      County&nbsp;Overview
    </router-link>
    <div class="top-spacer-dot-3 flex-group">
      <h2 class="center width-100-percent">
        Advisors
      </h2>
      <a
        :href="urlFor.economy"
      >
        Economist
      </a>
      <router-link :to="urlFor.infrastructure">
        City&nbsp;Planner
      </router-link>
      <a
        :href="urlFor.military"
      >
        War
      </a>
      <a
        :href="urlFor.infiltration"
      >
        Thieves Guild
      </a>
      <a
        :href="urlFor.casting"
      >
        Wizard Council
      </a>
      <a
        :href="urlFor.research"
      >
        Scientist
      </a>
    </div>
    <div
      v-if="user.isKing"
      class="top-spacer-dot-3"
    >
      <img
        class="resource_icons"
        src="/static/dist/images/crown_icon.jpg"
      >
      <a :href="urlFor.royalCourt">Royal Court</a>
    </div>
    <div class="top-spacer-dot-3 flex-group">
      <h2 class="center width-100-percent">
        Diplomacy
      </h2>
      <a
        :href="urlFor.trading"
      >
        Trades
      </a>
      <a
        :href="urlFor.messages"
        :class="{ bold: user.hasMail }"
      >
        Messages
      </a>
      <a
        :href="urlFor.chatroomAPI"
        :class="{ bold: user.hasChatMessage }"
      >
        Town&nbsp;Hall
      </a>
      <a
        class="mobile-link"
        :href="urlFor.kingdom"
      >
        Kingdom&nbsp;Overview
      </a>
    </div>
    <div class="top-spacer-dot-3 flex-group">
      <h2 class="center width-100-percent">
        About the Game
      </h2>
      <a
        :href="urlFor.achievements"
      >
        Achievements
      </a>
      <a
        :href="urlFor.forum"
      >
        Forum
      </a>
      <a :href="urlFor.guide">Player&nbsp;Guide</a>
      <a :href="urlFor.leaderboard">Leaderboard</a>
      <a :href="urlFor.profile">Profile</a>
      <a
        v-if="user.isAdmin"
        :href="urlFor.adminHomeAPI"
      >Admin</a>
    </div>
    <div class="top-spacer-dot-3" />
    <a :href="urlFor.logout">Logout</a>
  </nav>
</template>

<script>
export default {
  name: 'NavBar',
  data () {
    return {
      urlFor: Object,
      user: Object,
      errors: Object
    }
  },
  beforeCreate () {
    // if development
    // url is 'http://localhost:5000/api/sidebar' - happens auto-magically.
    this.$getData('/api/sidebar', this.$deployData)
  }
}
</script>
