<style scoped>
#side-bar {  /* The main sidebar which is always visible when logged in */
    display: flex;
    flex-direction: column;
    align-items: center;

    font-size: 1.5em;
    margin: 0 1em 0.3em 0.5em;
    padding: 0.6em;
    font-size: 1.25em;
    line-height: 1.7em;
    border: solid;
    border-radius: 5px;
}

.bold {
    font-weight: bold;
}

.text-center {
    text-align: center;
}

.spacer {
    margin-bottom: 1em;
}
</style>

<template>
  <nav
    id="side-bar"
    class=".text-center"
  >
    <a :href="urlFor.overview">
      County&nbsp;Overview
    </a>
    <h2>Advisors</h2>
    <a :href="urlFor.economy">
      Economist
    </a>
    <a :href="urlFor.infrastructure">
      City Planner
    </a>
    <a :href="urlFor.military">
      War
    </a>
    <a :href="urlFor.infiltration">
      Thieves Guild
    </a>
    <a :href="urlFor.magic">
      Wizard Council
    </a>
    <a :href="urlFor.research">
      Scientist
    </a>
    <h2>Diplomacy</h2>
    <a :href="urlFor.diplomacy">
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
    <a :href="urlFor.kingdom">
      Kingdom&nbsp;Overview
    </a>
    <div class="spacer" />
    <h2>About the Game</h2>
    <a :href="urlFor.achievements">
      Achievements
    </a>
    <a :href="urlFor.forum">
      Forum
    </a>
    <a :href="urlFor.guide">
      Player&nbsp;Guide
    </a>
    <a :href="urlFor.leaderboard">
      Leaderboard
    </a>
    <a :href="urlFor.versions">
      Read&nbsp;About&nbsp;Updates
    </a>
    <a
      v-if="user.isAdmin"
      :href="urlFor.adminHomeAPI"
    >
      Admin
    </a>
    <a :href="urlFor.logout">
      Logout
    </a>
  </nav>
</template>

<script>
export default {
  name: 'SideBar',
  data () {
    return {
      urlFor: Object,
      user: Object,
      errors: Object
    }
  },
  beforeCreate () {
    // if development
    // this.axios.get('http://localhost:5000/api/sidebar')
    this.$getData('/api/sidebar', this.$deployData)
  }
}
</script>
