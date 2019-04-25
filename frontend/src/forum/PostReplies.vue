<template>
  <div id="post-replies">
    <div
      v-for="reply in replies"
      :key="reply.id"
      class="reply"
    >
      <div class="body">
        <div
          class="content"
        >
          <forum-vote
            :votes="reply.votes"
            :up-vote="reply.upVote"
            @voted="updateVote(reply.id)"
          />
          {{ reply.content }}
        </div>
      </div>
      <most-recent-post
        class="most-recent-post"
        :post="reply"
      />
      <hr class="border-dotted width-100-percent">
    </div>
    <br>
    <message-input
      title=""
      :title-input="false"
      button-label="Reply to Post"
      :post-url="`/api/forum/posts?thread_id=${thread_id}&post_id=${post_id}`"
      @message-sent="fetchPosts"
    />
    <br>
  </div>
</template>

<script>
import MostRecentPost from './MostRecentPost.vue'
import MessageInput from '@/components/MessageInput.vue'
import ForumVote from './ForumVote.vue'

export default {
  name: 'PostReplies',
  components: {
    MostRecentPost,
    MessageInput,
    ForumVote,
  },
  data () {
    return {
      post: null,
      replies: null,
    }
  },
  computed: {
    post_id () {
      return this.$route.params.post_id
    },
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
      return this.$hydrate('/api/forum/replies?post_id=' + this.post_id)
    },
    updateVote (id) {
      this.axios.get('/api/forum/upvote/' + id)
    }
  }
}
</script>

<style scoped>
.most-recent-post {
  margin-left: auto;
}

@media (max-width: 640px) {
  .reply {
    display: flex;
    flex-direction: column;
  }

  .content {
    font-size: 1.2em;
    margin: 0.3em 0 0.3em;
  }
}

@media (min-width: 640px) {
  .reply {
    display: flex;
    flex-wrap: wrap;
  }

  .body {
    display: flex;
  }

  .center {
    margin-left: auto;
    margin-right: auto;
  }

  .content {
    font-size: 1.2em;
    padding-right: 1em;
  }

  .most-recent-post {
    margin-top: auto;
    flex-shrink: 0;
  }
}
</style>
