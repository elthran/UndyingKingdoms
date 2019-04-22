<template>
  <div id="forum">
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
      class="width-100-percent hide-last-hr"
      @push-trail="pushTrail"
    />
    <thread-posts
      v-else-if="threadView"
      class="hide-last-hr"
      @push-trail="pushTrail"
    />
    <post-replies
      v-else-if="postView"
      class="hide-last-hr"
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
      console.log("$route", from, to)
      // react to route changes ..
    },
    routingTrail (newVal, oldVal) {
      console.log("routingTrail", oldVal, newVal)
    },
  },
  mounted () {
    this.$hydrate(`/api/forum/routing?thread_id=${this.thread_id}&post_id=${this.post_id}`)
    .then(() => {
      // do something after hydration
    })
  },
  methods: {
    pushTrail (newTrail) {
      console.log("new trail", newTrail)
      this.$router.push(newTrail.url)
      this.routingTrail.push(newTrail)
    },
    popTrail (newTrail) {
      // go back one route.
      console.log(newTrail)
      this.$router.push(newTrail.url)
      this.routingTrail.splice(-newTrail.level, newTrail.level)
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
  /deep/ .hide-last-hr > div:last-child > hr:last-child {
    display: none;
  }

}

@media (min-width: 640px) {
  #forum {
    margin: 1.2em 1em;
  }

  .crumb-trail {
    text-align: center;
  }
}
</style>
