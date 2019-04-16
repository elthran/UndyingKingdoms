<template>
  <div id="chatlist">
    <tool-tip
      v-for="message in messages"
      :key="message.id"
      :tip="formatDate(message.time)"
      :bounder="self"
      align="mouse"
      style="border-bottom:none; color:black; width:100%;"
    >
      <vue-markdown>[{{ message.leader }}]({{ message.leaderUrl }}): {{ message.content }}</vue-markdown>
      <br v-if="newSpeaker">
    </tool-tip>
  </div>
</template>

<script>
import ToolTip from '@/components/ToolTip.vue'
import VueMarkdown from 'vue-markdown'

export default {
  name: 'ChatList',
  components: {
    ToolTip,
    VueMarkdown,
  },
  props: {
    messages: null
  },
  data () {
    return {
      self: null
    }
  },
  mounted () {
    this.self = this.$el
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
