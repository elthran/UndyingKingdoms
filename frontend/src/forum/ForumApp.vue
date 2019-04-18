<template>
  <div id="content">
    <!-- Show list of all threads -->
    <h1>Forum</h1>
    <table class="border-dotted width-100-percent max-width-500">
      <tr>
        <th>Thread</th>
        <th>Author</th>
        <th>Most Recent Post</th>
        <th>Number of Posts</th>
      </tr>
      <tr
        v-for="thread in threads"
        :key="thread.id"
      >
        <td><a :href="thread.url">{{ thread.title }}</a></td>
        <td>{{ thread.author }}</td>
        <td>{{ thread.mostRecentPost }}</td>
        <td>{{ thread.postCount }}</td>
      </tr>
    </table>
  </div>
</template>

<script>
export default {
  name: 'ForumApp',
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
  }
}
</script>
