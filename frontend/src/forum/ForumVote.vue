<template>
  <div id="forum-vote">
    <div
      class="arrow up"
      :class="{ active: upVote + vote }"
      @click="vote = 1 - upVote"
    />
    <span class="center">{{ votes + vote }}</span>
    <div
      class="arrow down"
      @click="vote = 0 - upVote"
    />
  </div>
</template>

<script>
export default {
  name: 'ForumVote',
  props: {
    votes: Number,
    upVote: Number,
  },
  data () {
    return {
      vote: 0,
    }
  },
  watch: {
    vote () {
      this.$emit('voted')
    }
  }
}
</script>


<style scoped>
#forum-vote {
  display: inline-flex;
  flex-direction: column;
  margin-top: 0.2em;
  margin-right: 0.6em;
  float: left;
}

.arrow {
  border: solid black;
  border-width: 0 3px 3px 0;
  display: inline-block;
  padding: 0.4em;
  cursor: pointer;
  /*width: 1em;
  height: 1em;*/
}

.arrow:active {
  position: relative;
  top: 1px;
}

.right {
  transform: rotate(-45deg);
  -webkit-transform: rotate(-45deg);
}

.left {
  transform: rotate(135deg);
  -webkit-transform: rotate(135deg);
}

.up {
  transform: rotate(-135deg);
  -webkit-transform: rotate(-135deg);
}

.down {
  transform: rotate(45deg);
  -webkit-transform: rotate(45deg);
}

.active {
  box-shadow: -2px -2px 3px #FFD700 inset;
}

@media (max-width: 640px) {
  #forum-vote {

  }
}
</style>
