<template>
  <div id="thread-posts">
    <div
      v-for="post in posts"
      :key="post.id"
      class="post"
    >
      <forum-stats
        :votes="post.votes"
        :reply-count="post.replyCount"
        :views="post.views"
      />
      <div
        class="center title"
      >
        <a
          :href="post.url"
          @click.prevent="$emit('push-trail', { url: post.url, name: post.title })"
        >
          {{ post.title }}
        </a>
      </div>
      <most-recent-post
        class="most-recent-post"
        :post="post.mostRecentReply"
      />
      <hr class="border-dotted width-100-percent">
    </div>
    <br>
    <message-input
      title="Create New Thread"
      :post-url="`/api/forum/posts?thread_id=${thread_id}`"
      @message-sent="fetchPosts"
    />
    <br>
  </div>
</template>

<script>
import MostRecentPost from './MostRecentPost.vue'
import MessageInput from '@/components/MessageInput.vue'
import ForumStats from './ForumStats.vue'

export default {
  name: 'ThreadPosts',
  components: {
    MostRecentPost,
    MessageInput,
    ForumStats,
  },
  data () {
    return {
      thread: null,
      posts: null,
    }
  },
  computed: {
    thread_id () {
      return this.$route.params.thread_id
    },
  },
  mounted () {
    this.fetchPosts()
    .then(() => {
      // do something interesting
    })
  },
  methods: {
    fetchPosts () {
      return this.$hydrate('/api/forum/posts?thread_id=' + this.thread_id)
    }
  }
}
</script>

<style scoped>
.most-recent-post {
  margin-left: auto;
}

@media (max-width: 640px) {
  .post {
    display: flex;
    flex-direction: column;
  }

  .title {
    font-size: 1.3em;
    margin: 0.3em 0 0.3em
  }
}

@media (min-width: 640px) {
  .post {
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
