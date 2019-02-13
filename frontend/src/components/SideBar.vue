<style type="text/css">
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

.notice {
    font-weight:bold;
}

.center-text {
  text-align: center;
}
</style>

<template>
  <div id="layout-body">
    <div id="sidebar">
      <ul class="center-text">
        <li><a :href="url_for('overview', kingdom_id=0, county_id=0)">County&nbsp;Overview</a></li>
        <li><a :href="url_for('economy')">Economy</a></li>
        <li><a :href="url_for('infrastructure')">Infrastructure</a></li>
        <li><a :href="url_for('military')">Military</a></li>
        <li><a :href="url_for('infiltration')">Infiltration</a></li>
        <li><a :href="url_for('messages')" v-bind:class="{ notice: hasMail }">Inbox</a></li>
        <li><a :href="url_for('chatroom_api')">Town&nbsp;Hall</a></li>
        <li><a :href="url_for('kingdom', kingdom_id=kingdomId)">Kingdom&nbsp;Overview</a></li>
        <li><br></li>
        <li><h1>About the Game</h1></li>
        <li><a :href="url_for('achievements')">Achievements</a></li>
        <li><a :href="url_for('forum', thread_id=0, post_id=0)">Forum</a></li>
        <li><a :href="url_for('guide')">Player&nbsp;Guide</a></li>
        <li><a :href="url_for('leaderboard')">Leaderboard</a></li>
        <li><a :href="url_for('versions')">Read&nbsp;About&nbsp;Updates</a></li>
        {% if user.is_admin %}<li><a :href="url_for('admin.home_api')">Admin</a></li>{% endif %}
        <li><a :href="url_for('logout')">Logout</a></li>
        <li><br><br><br></li>
      </ul>
    </div>
    <div id="layout-content">
      {% block content2 %}
      {% endblock %}
    </div>
  </div>
</template>

<script>
import axios from 'axios';
// import _ from 'lodash';

export default {
  name: "SideBar",
  props: {
    hasMail: Boolean,
    content: String,
    kingdomId: Number
  /*
  has_mail
  {% set user = current_user %}
{% set county = current_user.county %}
{% set kingdom = county.kingdom %}
is_admin
  */
  },
  methods: {
    url_for: function () {
      axios.post('/api/url_for', arguments
      )
      .then(function (response) {
        console.log(response);
      })
      .catch(function (error) {
        console.log(error);
      })
    }
  }
}
</script>
