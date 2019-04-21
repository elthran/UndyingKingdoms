<template>
  <div id="forum-threads">
    <div
      v-for="thread in threads"
      :key="thread.id"
      class="thread"
    >
      <div class="stats">
        <div>{{ thread.votes }} votes</div>
        <div class="highlight">
          {{ thread.postCount }} posts
        </div>
        <div>{{ thread.views || 'xx' }} views</div>
      </div>
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
        class="most-recent-post"
        :post="thread.mostRecentPost"
      />
      <hr class="border-dotted width-100-percent">
    </div>
  </div>
</template>

<script>
import MostRecentPost from './MostRecentPost.vue'

export default {
  name: 'ForumThreads',
  components: {
    MostRecentPost
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
.highlight {
  border: solid LightGrey 1px;
  border-radius: 0.5em;
  padding: 0.2em;
}

.most-recent-post {
  margin-left: auto;
}

@media (max-width: 640px) {
  .thread {
    display: flex;
    flex-direction: column;
  }

  .stats {
    display: flex;
  }

  .highlight {
    margin-left: 0.3em;
    margin-right: 0.3em;
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

  .stats {
    display: flex;
    flex-direction: column;
    align-items: center;
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
