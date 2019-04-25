<template>
  <div id="forum">
    <prefix-title title="Forum" />
    <!-- Show list of all threads -->
    <h1 class="crumb-trail">
      <crumb-trail
        :trail="routingTrail"
        @pop-trail="popTrail"
      />
    </h1>
    <hr>
    <forum-threads
      v-if="forumView"
      class="hide-last-hr side-margins"
      @push-trail="pushTrail"
    />
    <thread-posts
      v-else-if="threadView"
      class="hide-last-hr side-margins"
      @push-trail="pushTrail"
    />
    <post-replies
      v-else-if="postView"
      class="hide-last-hr side-margins"
      @push-trail="pushTrail"
    />
  </div>
</template>

<script>
import ForumThreads from './ForumThreads.vue'
import ThreadPosts from './ThreadPosts.vue'
import PostReplies from './PostReplies.vue'
import CrumbTrail from '@/components/CrumbTrail.vue'

export default {
  name: 'ForumApp',
  components: {
    ForumThreads,
    ThreadPosts,
    PostReplies,
    CrumbTrail,
  },
  data () {
    return {
      routingTrail: [{
        name: "Forum",
        url: ''
      }]
    }
  },
  computed: {
    thread_id () {
      return this.$route.params.thread_id
    },
    post_id () {
      return this.$route.params.post_id
    },
    forumView () {
      return this.thread_id == 0 && this.post_id == 0
    },
    threadView () {
      return this.thread_id > 0 && this.post_id == 0
    },
    postView () {
      return this.thread_id > 0 && this.post_id > 0
    },
  },
  watch: {
    $route (to, from) {
      this.$hydrate(`/api/forum/routing?thread_id=${to.params.thread_id}&post_id=${to.params.post_id}`)
    }
  },
  mounted () {
    this.$hydrate(`/api/forum/routing?thread_id=${this.thread_id}&post_id=${this.post_id}`)
    .then(() => {
      // do something after hydration
    })
  },
  methods: {
    // add route to trail
    pushTrail (newTrail) {
      this.$router.push(newTrail.url)
    },
    // go back up "level" routes.
    popTrail (newTrail) {
      this.$router.push(newTrail.url)
    }
  },
}
</script>

<style scoped>
.highlight {
  border: solid LightGrey 1px;
  border-radius: 0.5em;
  padding: 0.2em;
}

@media (max-width: 640px) {
  #forum {
    margin: 1.2em 1em 0;
  }

  /* remove the last hr in the forum */
  /*/deep/ .hide-last-hr > div:last-child > hr:last-child {
    display: none;
  }*/

}

@media (min-width: 640px) {
  #forum {
    width: 100%;
    margin: 1.2em 1em 0 0;
  }

  .crumb-trail {
    text-align: center;
  }

  .side-margins {
    margin-right: 1em;
  }

  /deep/ .most-recent-post {
    margin-right: 1em;
  }
}
</style>
