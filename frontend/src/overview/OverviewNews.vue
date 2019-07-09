<template>
  <!-- Need to create a news array for display, so I can check it for empty -->
  <ul>
    <template v-if="news.length">
      <li
        v-for="event in news"
        :key="event.id"
        class="hanging-indent"
      >
        Day: {{ event.day }} - <span v-html="event.title" />: {{ event.content }}
      </li>
    </template>
    <li v-else>
      No new events to report.
    </li>
  </ul>
</template>

<script>
export default {
  name: 'OverviewNews',
  props: {
    news: Array
  }
}
</script>
