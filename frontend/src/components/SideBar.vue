<style scoped>
#side-bar {  /* The main sidebar which is always visible when logged in */
    display: flex;
    flex-direction: column;
    align-items: center;

    font-size: 1.5em;
    margin: 0 1em 0.5em;
    margin-right: 1em;
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
  <nav id="side-bar" class=".text-center">
    <h1>Gameplay</h1>
    <a :href="urlFor.overview">County&nbsp;Overview</a>
    <a :href="urlFor.economy">Economy</a>
    <a :href="urlFor.infrastructure">Infrastructure</a>
    <a :href="urlFor.military">Military</a>
    <a :href="urlFor.infiltration">Infiltration</a>
    <a :href="urlFor.diplomacy">Diplomacy</a>
    <a :href="urlFor.messages"
       :class="{ bold: user.hasMail }"
    >Inbox</a>
    <a :href="urlFor.chatroomAPI"
       :class="{ bold: user.hasChatMessage }"
    >Town&nbsp;Hall</a>
    <a :href="urlFor.kingdom">Kingdom&nbsp;Overview</a>
    <div class="spacer"></div>
    <h1>About the Game</h1>
    <a :href="urlFor.achievements">Achievements</a>
    <a :href="urlFor.forum">Forum</a>
    <a :href="urlFor.guide">Player&nbsp;Guide</a>
    <a :href="urlFor.leaderboard">Leaderboard</a>
    <a :href="urlFor.versions">Read&nbsp;About&nbsp;Updates</a>
    <a v-if="user.isAdmin" :href="urlFor.adminHomeAPI">Admin</a>
    <a :href="urlFor.logout">Logout</a>
  </nav>
</template>

<script>
export default {
  name: "SideBar",
  data () {
    return {
      'urlFor': Object,
      'user': Object,
      'error': ''
    }
  },
  methods: {
    updatePage (data) {
      // console.log(data);
      this.urlFor = data.urlFor;
      this.user = data.user;
    }
  },
  mounted () {
    // if development
    // this.axios.get('http://localhost:5000/api/sidebar')
    this.axios.get('/api/sidebar')
    .then((response) => {
      if (response.status === 200) {
        this.updatePage(response.data);
      } else {
        console.log(response);
      }
    })
    .catch((error) => {
      console.log(error.response);
    });
  }
}
</script>
