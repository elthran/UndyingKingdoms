<template>
  <div
    id="chatroom"
    :style="{ maxHeight: correctedHeight }"
  >
    <prefix-title title="Town Hall" />
    <div id="header">
      <h1>Discussion</h1>
      <toggle-swtich
        v-model="globalChatOn"
        on-label="global"
        off-label="kingdom"
      />
    </div>
    <div
      id="chat-div"
      ref="chatDiv"
    >
      <chat-list :messages="filteredMessages" />
    </div>
    <br>
    <csrf-token :value="CSRFToken" />
    <input
      id="content"
      v-model="message"
      class="form-control"
      name="content"
      placeholder="Public to your kingdom"
      required
      autofocus
      type="text"
      @keyup.enter="sendMessage"
    >
    <br><br>
    <button
      id="send"
      type="submit"
      @click="sendMessage"
    >
      Send Herald
    </button>
  </div>
</template>

<script>
import ToggleSwitch from '@/components/ToggleSwitch.vue'
import CSRFToken from '@/components/CSRFToken.vue'
import ChatList from './ChatList.vue'

export default {
  name: 'ChatroomApp',
  components: {
    'toggle-swtich': ToggleSwitch,
    'csrf-token': CSRFToken,
    'chat-list': ChatList
  },
  data () {
    return {
      CSRFToken: '',
      globalChatOn: true,
      messages: [],
      message: '',
      leader: null,
      timestamp: null,
      toggleWatcher: null,
      windowHeight: window.innerHeight,
      pad: 10,
      scrolled: false,
      clock: {
        handle: null,
        run: this.runClock
      },
    }
  },
  computed: {
    filteredMessages () {
      return this.messages.filter((m) => this.globalChatOn ? m.room === 'global' : m.room === 'kingdom')
    },
    lastMessageId () {
      var id = this.messages.slice(-1)[0].id
      return id === undefined ? 0 : id
    },
    correctedHeight () {
      return (this.windowHeight - 30) + 'px'
    },
    chatDiv () {
      return this.$refs.chatDiv
    }
  },
  mounted () {
    this.$hydrate('/api/chatroom/update')
    .then(() => {
      this.scrollToMax()
      this.toggleWatcher = this.$watch('globalChatOn', this.updateChat)
    })

    this.$nextTick(() => {
      window.addEventListener('resize', this.onResize)
      this.chatDiv.addEventListener('scroll', this.onScroll)
      // Active update function when the window gains focus.
      window.addEventListener("focus", this.startClock)
      // Stop update function when the window loses focus.
      window.addEventListener("blur", this.stopClock)
    })
  },
  beforeDestroy () {
    window.removeEventListener('resize', this.onResize)
    this.chatDiv.removeEventListener('scroll', this.onScroll)
    window.removeEventListener("focus", this.startClock)
    window.removeEventListener("blur", this.stopClock)
    this.stopClock()
  },
  methods: {
    startClock () {
      this.clock.handle = this.clock.run()
    },
    stopClock () {
      clearInterval(this.clock.handle)
    },
    runClock () {
      console.log("running clock")
      this.getNewMessages()  // run immediately on focus, then every x seconds.
      return setInterval(this.getNewMessages, 5000);
    },
    // refocus(selector) {
    //   if (!scrolled) {
    //     var yOffset = $(selector).offset().top + $(selector).height() + pad;
    //     $('html, body').animate({
    //         scrollTop: yOffset - window.innerHeight
    //     })
    //   }
    // },
    // Scroll window to bottom if user hasn't scrolled around.
    // not sure if nextick should be here or in caller.
    scrollToMax() {
      this.$nextTick(() => {
        if (!this.scrolled) {
          this.chatDiv.scrollTop = this.chatDiv.scrollHeight-this.chatDiv.clientHeight;
        }
      })
    },
    updateChat () {
      // console.log('updating chat')
      this.$sendData({
        csrf_token: this.CSRFToken,
        global_chat_on: this.globalChatOn,
        action: '/api/chatroom/update',
      })
      .catch((error) => {
        if (error.response.status === 303) {
          return 0
        } else {
          console.log("updateChat errors:", error, error.response)
          return Promise.reject(error)
        }
      })
      // always run this, in parallel
      this.getNewMessages()
    },
    sendMessage () {
      var content = this.message
      this.message = ''
      this.$sendData({
        csrf_token: this.CSRFToken,
        global_chat_on: this.globalChatOn,
        content: content,
        action: '/api/chatroom/update',
        last_message_id: this.lastMessageId,
      })
      .then((data) => {
        // console.log("Send message response:", data)
        return this.getNewMessages()
      })
    },
    getNewMessages () {
      // console.log("getNewMessages")
      return this.$getData('/api/chatroom/update?last_message_id=' + this.lastMessageId)
      .then((data) => {
        // console.log("new messages:", data)
        this.messages = this.messages.concat(data.messages)
        this.scrollToMax();
        // refocus("#send");
      })
      .catch((error) => { console.log(error); Promise.reject(error) })
    },
    onResize () {
      this.windowHeight = window.innerHeight
    },
    // Disabled auto-scrolling if user has scrolled content.
    // Re-enable it if they scroll to the bottom.
    onScroll () {
      if (this.chatDiv.scrollTop >= this.chatDiv.scrollHeight - this.chatDiv.clientHeight) {
          this.scrolled = false;
      } else {
          this.scrolled = true;
      }
    },
  },
}
</script>

<style scoped>
@media (max-width: 640px) {
  #chatroom {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin: 1.2em 1em;
  }

  #header {
    display: flex;
    justify-content: space-between;
    width: 100%;
    /*max-width: 320px;*/
    margin-bottom: 1em;
  }

  h1 {
    margin-bottom: 0;
  }

  #chat-div {
    width: 100%;
    max-width: 500px;
    /*max-height: 15em;*/
    overflow-y: auto;
  }

  #content {
    padding: 1em;
    width: 100%;
    border-radius: 0.5em;
    margin-bottom: 0.4em;
    margin: 1em;
  }

  button {
    width: 100%;
    height: 3em;
    border-radius: 0.5em;
  }

  .tab {
    margin-left: 1em;
  }
}

@media (min-width: 640px) {
  #layout-content {
    display: flex;
    justify-content: space-around;
  }

  #chatroom {
    max-width: 40em;
  }

  #header {
    display: flex;
    justify-content: space-between;
    padding-top: 1em;
    margin-bottom: 1em;
  }

  #chat-div {
    border:solid 1px;
    min-height: 300px;
    min-width: 600px;
    max-height: 750px;
    overflow-y: auto;
  }
}
</style>