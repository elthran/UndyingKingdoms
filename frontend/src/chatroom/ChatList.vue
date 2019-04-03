<template>
  <ul
    id="chatlist"
    class="dont-break-out"
  >
    <li
      v-for="message in messages"
      :key="message.id"
    >
      ({{ formatDate(message.time) }}) {{ message.leader }}: {{ message.content }}
    </li>
  </ul>
</template>

<script>
export default {
  name: 'ChatList',
  props: {
    messages: [Array]
  },
  data () {
    return {

    }
  },
  methods: {
    formatDate(time) {
      var date = new Date(time + "Z");
      var hours = ("0" + date.getHours()).slice(-2);
      var minutes = ("0" + date.getMinutes()).slice(-2);
      var seconds = ("0" + date.getSeconds()).slice(-2);

      return hours + ":" + minutes + ":" + seconds;
    }
  }
}
</script>

<style>
@media (max-width: 640px) {
  #chatlist {
    border: solid 1px;
    border-radius: 4px;
    padding: 0.4em;
    min-height: 14em;
    width: 100%;
  }
}
</style>
