<template>
  <nav
    id="mobile-navbar"
    class="invisible"
  >
    <hr class="width-95-percent">
    <router-link
      :to="urlFor.overview"
    >
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
      <!-- <router-link
        :to="urlFor.infrastructure"
      >
        City&nbsp;Planner
      </router-link> -->
      <a :href="urlFor.infrastructure">City&nbsp;Planner</a>
      <!-- <router-link
        :to="urlFor.military"
      >
        War
      </router-link> -->
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
      <router-link
        :to="urlFor.research"
      >
        Scientist
      </router-link>
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
        @click.native="user.hasMail = false"
      >
        Messages
      </a>
      <router-link
        :to="urlFor.chatroom"
        :class="{ bold: user.hasChatMessage }"
        @click.native="user.hasChatMessage = false"
      >
        Town&nbsp;Hall
      </router-link>
      <a
        class="mobile-link"
        :href="urlFor.kingdom"
      >
        Kingdom&nbsp;Overview
      </a>
      <div
        v-if="user.isKing"
        class="top-spacer-dot-3 center"
      >
        <img
          class="resource_icons"
          src="/static/dist/images/crown_icon.jpg"
        >
        <a :href="urlFor.royalCourt">Royal Court</a>
      </div>
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
      <router-link
        :to="urlFor.forum"
      >
        Forum
      </router-link>
      <a :href="urlFor.guide">Player&nbsp;Guide</a>
      <a :href="urlFor.leaderboard">Leaderboard</a>
      <a :href="urlFor.profile">Profile</a>
      <a
        v-if="user.isAdmin"
        :href="urlFor.adminHomeAPI"
      >Admin</a>
      <a
        :href="urlFor.clan"
      >
        <span v-if="user.hasClan">
          Clan
        </span>
        <span v-else>
          Create Kingdom
        </span>
      </a>
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
      urlFor: {
        overview: '',
        infrastructure: '',
        chatroom: '',
        forum: '',
        research: '',
      },
      user: Object,
    }
  },
  mounted () {
    // if development
    // url is 'http://localhost:5000/api/navbar' - happens auto-magically.
    this.$hydrate('/api/navbar')
    .then(() => {
      this.$el.classList.remove('invisible')
    })
  },
}
</script>

<style scoped>
/* The main navbar which is always visible when logged in */
/* Converts to bottom navigation on small screens */
@media (max-width: 640px) {
  #mobile-navbar {
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
    /*text-decoration: none;*/
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
}

/* Make nav bar into a sidebar on larger screens */
@media (min-width: 640px) {
  #mobile-navbar {
    display: flex;
    flex-direction: column;
    align-items: center;

    margin: 0.5em 1em 0.5em 0.5em;
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

  hr {
    display: none;
  }

  .flex-group {
    display: flex;
    flex-direction: column;
    justify-content: center;
  }

  a {
    text-align: center;
  }
}
</style>
