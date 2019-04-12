<template>
  <ul id="chatlist">
    <li
      v-for="message in messages"
      :key="message.id"
    >
      <tool-tip
        :tip="'(' + formatDate(message.time) + ')'"
        align="right"
        style="border-bottom: none;color: black;width: 100%;"
      >
        {{ message.leader }}: {{ message.content }}
      </tool-tip>
    </li>
  </ul>
</template>

<script>
import ToolTip from '@/components/ToolTip.vue'

export default {
  name: 'ChatList',
  components: {
    'tool-tip': ToolTip,
  },
  props: {
    messages: null
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

<style scoped>
#chatlist {
  border: solid 1px;
  border-radius: 4px;
  padding: 0.4em;
  min-height: 14em;
  width: 100%;
}
</style>
