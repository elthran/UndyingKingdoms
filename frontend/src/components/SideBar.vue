<template>
  <div id="sidebar">
    <ul class=".text-center">
      <li><h1>Gameplay</h1></li>
      <li><a :href="urlFor.overview">County&nbsp;Overview</a></li>
      <li><a :href="urlFor.economy">Economy</a></li>
      <li><a :href="urlFor.infrastructure">Infrastructure</a></li>
      <li><a :href="urlFor.military">Military</a></li>
      <li><a :href="urlFor.infiltration">Infiltration</a></li>
      <li><a :href="urlFor.diplomacy">Diplomacy</a></li>
      <li>
        <a :href="urlFor.messages"
           :class="{ bold: user.hasMail }"
        >Inbox</a>
      </li>
      <li>
        <a :href="urlFor.chatroomAPI"
           :class="{ bold: user.hasChatMessage }"
        >Town&nbsp;Hall</a>
      </li>
      <li><a :href="urlFor.kingdom">Kingdom&nbsp;Overview</a></li>
      <li><br></li>
      <li><h1>About the Game</h1></li>
      <li><a :href="urlFor.achievements">Achievements</a></li>
      <li><a :href="urlFor.forum">Forum</a></li>
      <li><a :href="urlFor.guide">Player&nbsp;Guide</a></li>
      <li><a :href="urlFor.leaderboard">Leaderboard</a></li>
      <li><a :href="urlFor.versions">Read&nbsp;About&nbsp;Updates</a></li>
      <li v-if="user.isAdmin">
        <a :href="urlFor.adminHomeAPI">Admin</a>
      </li>
      <li><a :href="urlFor.logout">Logout</a></li>
      <li><br><br><br></li>
    </ul>
  </div>
</template>

<script>
export default {
  name: "SideBar",
  data () {
    return {
      'urlFor': Object,
      'user': Object
    }
  },
  methods: {
    updatePage (data) {
      console.log(data);
      this.urlFor = data.urlFor;
      this.user = data.user;
    }
  },
  mounted () {
    this.axios.get('/api/sidebar')
    .then((response) => {
      if (response.status === 200) {
        this.updatePage(response.data);
      } else {
        console.log(response);
      }
    })
    .catch(function (error) {
      // handle error
      console.log(error);
    });
  }
}
</script>

<style scoped>
#layout-body {
    display: flex;
    margin: 1em;
}

#sidebar {  /* The main sidebar which is always visible when logged in */
    margin-right: 1em;
    padding: 0.6em;
    font-size: 1.25em;
    line-height: 1.7em;
    border: solid;
    border-radius: 5px;
}

#layout-content {
    width: 100%;
}

.bold {
    font-weight: bold;
}

.text-center {
    text-align: center;
}
</style>
