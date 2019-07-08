<template>
  <div>
    {{ formatedTime(post.timeCreated) }} by <a :href="post.leaderUrl">{{ post.author }}</a>
  </div>
</template>

<script>
export default {
  name: 'MostRecentPost',
  props: {
    post: Object,
  },
  methods: {
    formatedTime (time) {
      var msDiff = new Date() - new Date(time);
      var days = Math.floor(msDiff / (1000*60*60*24))
      if (days >= 1) {
        return days + (days > 1 ? " days" : " day")
      }
      var hours = Math.floor(msDiff / (1000*60*60))
      if (hours >= 1) {
        return hours + (hours > 1 ? " hours" : " hour")
      }
      var minutes = Math.floor(msDiff / (1000*60))
      if (minutes >= 1) {
        return minutes + (minutes > 1 ? " minutes" : " minute")
      }
      var seconds = Math.floor(msDiff / (1000))
      return seconds + (seconds > 1 ? " seconds" : " second")
    },
  },
}
</script>
