<template>
  <div id="chatlist">
    <div
      v-for="(group, index) in groups"
      :key="index"
      class="grouping"
    >
      <tool-tip
        v-for="(message, mindex) in group"
        :key="message.id"
        :tip="message.leader + ' - ' + formatDate(message.time)"
        :bounder="self"
        align="mouse"
        class="message"
      >
        <a
          v-if="mindex === 0"
          :href="message.leaderUrl"
          class="badge"
        >
          {{ message.leader }}
        </a>
        <vue-markdown
          class="inline"
          :source="message.content"
        />
      </tool-tip>
    </div>
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
      self: null,
    }
  },
  computed: {
    // There's probably a better way.(tm)
    groups () {
      var speaker = null
      var group = []
      var groups = []
      this.messages.forEach(
        function (currentValue, index) {
          if (speaker !== currentValue.leader) {
            speaker = currentValue.leader
            // only the first time of each set
            if (group.length === 0) {
              group.push(currentValue)
            } else {
              groups.push(group)
              group = []
              group.push(currentValue)
            }
          } else {
            group.push(currentValue)
          }
        }
      )
      if (group.length > 0) {
        groups.push(group)
        group = []
      }
      return groups
    }
  },
  created () {
    this.newSpeaker = false;
  },
  mounted () {
    this.self = this.$el
  },
  methods: {
    formatDate (time) {
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

#chatlist :first-child {
  margin-top: 0 !important;
}

.message {
  width: 100%;
  color: black;
  border-bottom: none;
}

.grouping {
  margin-top: 0.4em;
  border: 1px solid #ccc;
  box-shadow: outset 0 1px 3px #ddd;
  padding: 0.6em;
  border-radius: 5px;
}

.badge {
  margin-right: 0.3em;
}

.inline, .inline :first-child {
  display: inline;
}
</style>
