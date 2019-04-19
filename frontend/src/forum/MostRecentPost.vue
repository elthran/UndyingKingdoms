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
      var date = new Date(time + "Z");
      var hours = ("0" + date.getHours()).slice(-2);
      var minutes = ("0" + date.getMinutes()).slice(-2);
      var seconds = ("0" + date.getSeconds()).slice(-2);
      if (hours >= 1) {
        return hours + (hours > 1 ? " hours" : " hour")
      } else if (minutes >= 1) {
        return minutes + (minutes > 1 ? " minutes" : " minute")
      } else {
        return seconds + (seconds > 1 ? " seconds" : " second")
      }
    },
  },
}
</script>
