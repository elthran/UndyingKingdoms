<template>
  <div class="stats">
    <div>
      {{ votes }} votes
    </div>
    <div
      v-if="replyCount"
      class="highlight"
    >
      {{ replyCount }} replies
    </div>
    <div
      v-if="views"
    >
      {{ views || 'xx' }} views
    </div>
  </div>
</template>

<script>
export default {
  name: "ForumStats",
  props: {
    votes: Number,
    replyCount: Number,
    views: Number,
  },
  data () {
    return {
    }
  }
}
</script>

<style scoped>
.highlight {
  border: solid LightGrey 1px;
  border-radius: 0.5em;
  padding: 0.2em;
}

@media (max-width: 640px) {
  .stats {
    display: flex;
  }

  .highlight {
    margin-left: 0.3em;
    margin-right: 0.3em;
  }
}

@media (min-width: 640px) {
  .stats {
    display: flex;
    flex-direction: column;
    align-items: center;
    flex-shrink: 0;
  }
}
</style>
