<template>
  <div id="forum">
    <!-- Show list of all threads -->
    <h1 class="center">
      <arrow-route :route="forumRoute" />
    </h1>
    <hr>
    <forum-threads
      v-if="allThreadsView"
      class="width-100-percent"
    />
    <thread-posts
      v-else-if="specificThreadView"
    />
  </div>
</template>

<script>
import ForumThreads from './ForumThreads.vue'
import ThreadPosts from './ThreadPosts.vue'
import ArrowRoute from '@/components/ArrowRoute.vue'

export default {
  name: 'ForumApp',
  components: {
    ForumThreads,
    ThreadPosts,
    ArrowRoute,
  },
  data () {
    return {
      root: ''
    }
  },
  computed: {
    thread_id () {
      return this.$route.params.thread_id
    },
    post_id () {
      return this.$route.params.post_id
    },
    allThreadsView () {
      return this.thread_id == 0 && this.post_id == 0
    },
    specificThreadView () {
      return this.thread_id > 0 && this.post_id == 0
    },
    specificPostView () {
      return this.thread_id > 0 && this.post_id > 0
    },
    forumRoute () {
      var route = []
      route.push({
        name: "Forum",
        url: this.root + '/0/0'
      })
      if (this.specificThreadView || this.specificPostView) {
        route.push({
          name: "Thread",
          url: this.root + `/${this.thread_id}/0`
        })
      }
      if (this.specificPostView) {
        route.push({
          name: "Post",
          url: this.root + `/${this.thread_id}/${this.post_id}`
        })
      }
      return route
    }
  },
  watch: {
    $route (to, from) {
      // react to route changes ..
    }
  },
  mounted () {
    this.$hydrate('/api/forum/routing')
    .then(() => {
      // do something interesting
    })
  },
}
</script>

<style>
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
  #forum .thread:last-child, .post:last-child hr:last-child {
    display: none;
  }
}

@media (min-width: 640px) {
  #forum {
    margin: 1.2em 1em;
  }
}
</style>
