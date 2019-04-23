<template>
  <div id="thread-posts">
    <div
      v-for="post in posts"
      :key="post.id"
      class="post"
    >
      <div class="stats">
        <div>{{ post.votes }} votes</div>
        <div class="highlight">
          {{ post.replyCount }} replies
        </div>
        <div>{{ post.views || 'xx' }} views</div>
      </div>
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
    />
  </div>
</template>

<script>
import MostRecentPost from './MostRecentPost.vue'
import MessageInput from '@/components/MessageInput.vue'

export default {
  name: 'ThreadPosts',
  components: {
    MostRecentPost,
    MessageInput,
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
    this.$hydrate('/api/forum/posts?thread_id=' + this.thread_id)
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
  .post {
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
  .post {
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
