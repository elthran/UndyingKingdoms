<template>
  <div id="post-replies">
    <div
      v-for="reply in replies"
      :key="reply.id"
      class="reply"
    >
      <div class="stats">
        <div>{{ reply.votes }} votes</div>
        <div class="highlight">
          {{ reply.replyCount }} replies
        </div>
        <div>{{ reply.views || 'xx' }} views</div>
      </div>
      <div
        class="content"
      >
        {{ reply.content }}
      </div>
      <most-recent-post
        class="most-recent-post"
        :post="reply"
      />
      <hr class="border-dotted width-100-percent">
    </div>
  </div>
</template>

<script>
import MostRecentPost from './MostRecentPost.vue'

export default {
  name: 'PostReplies',
  components: {
    MostRecentPost,
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
  },
  mounted () {
    this.$hydrate('/api/forum/replies?post_id=' + this.post_id)
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
  .reply {
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
    margin: 0.3em 0 0.3em;
  }
}

@media (min-width: 640px) {
  .reply {
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
