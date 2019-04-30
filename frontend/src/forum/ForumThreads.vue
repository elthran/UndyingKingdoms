<template>
  <div id="forum-threads">
    <div
      v-for="thread in threads"
      :key="thread.id"
      class="thread"
    >
      <forum-stats
        :votes="thread.votes"
        :reply-count="thread.postCount"
        :views="thread.views"
      />
      <div
        class="center title"
      >
        <a
          :href="thread.url"
          @click.prevent="$emit('push-trail', { url: thread.url, name: thread.title })"
        >
          {{ thread.title }}
        </a>
      </div>
      <most-recent-post
        v-if="thread.mostRecentPost"
        class="most-recent-post"
        :post="thread.mostRecentPost"
      />
      <hr class="border-dotted width-100-percent">
    </div>
  </div>
</template>

<script>
import MostRecentPost from './MostRecentPost.vue'
import ForumStats from './ForumStats.vue'

export default {
  name: 'ForumThreads',
  components: {
    MostRecentPost,
    ForumStats,
  },
  data () {
    return {
      threads: null,
    }
  },
  mounted () {
    this.$hydrate('/api/forum/threads')
    .then(() => {
      // do something interesting
    })
  },
}
</script>

<style scoped>
.most-recent-post {
  margin-left: auto;
}

@media (max-width: 640px) {
  .thread {
    display: flex;
    flex-direction: column;
  }

  .title {
    font-size: 1.3em;
    margin: 0.3em 0 0.3em
  }
}

@media (min-width: 640px) {
  .thread {
    display: flex;
    flex-wrap: wrap;
  }

  .center {
    margin-left: auto;
    margin-right: auto;
  }

  .title {
    font-size: 1.3em;
    padding-left: 1em;
    padding-right: 1em;
  }

  .most-recent-post {
    margin-top: auto;
  }
}
</style>
