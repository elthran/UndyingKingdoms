<template>
  <div
    id="chatroom"
    class="invisible"
    :style="{ maxHeight: correctedHeight + 'px' }"
  >
    <prefix-title title="Town Hall" />
    <div id="header">
      <h1>Discussion</h1>
      <toggle-switch
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
    <textarea
      id="input"
      v-model="message"
      class="form-control"
      name="content"
      placeholder="Public to your kingdom"
      :maxlength="maxLength"
      required
      autofocus
      @keyup.enter.exact="sendMessage"
      @keydown.ctrl.enter.exact="addNewline"
      @keydown.ctrl.shift.enter.exact="addNewline"
    />
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
    ToggleSwitch,
    'csrf-token': CSRFToken,
    ChatList,
  },
  data () {
    return {
      CSRFToken: '',
      maxLength: null,
      globalChatOn: true,
      messages: [],
      message: '',
      leader: null,
      timestamp: null,
      toggleWatcher: null,
      windowHeight: window.innerHeight,
      pad: 10,
      scrolled: false,
      clockHandle: null,
    }
  },
  computed: {
    filteredMessages () {
      return this.messages.filter((m) => this.globalChatOn ? m.room === 'global' : m.room === 'kingdom')
    },
    lastMessageId () {
      // crashes on first run
      try {
        return this.messages.slice(-1)[0].id
      } catch {
        return 0
      }
    },
    correctedHeight () {
      return (this.windowHeight - 30)
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
      this.$el.classList.remove('invisible')
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
      this.clockHandle = this.runClock()
    },
    stopClock () {
      clearInterval(this.clockHandle)
    },
    runClock () {
      // change the run method on second run
      // basically ignore the first run of this method.
      // This is to accomodate my poor coding style.
      this.runClock = () => {
        this.getNewMessages()  // run immediately on focus, then every x seconds.
        return setInterval(this.getNewMessages, 5000);
      }
    },
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
        return data
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
    addNewline () {
      this.message += '\n'
    }
  },
}
</script>

<style scoped>
#chat-div {
  width: 100%;
  height: 100%;
  overflow-x: hidden;
  overflow-y: auto;
  /* This is all I need to make words break properly ... */
  overflow-wrap: break-word;
}

#header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 1em;
  width: 100%
}

#chatroom {
  display: flex;
  flex-direction: column;
}

button {
  min-height: 3em;
}

#input {
  padding: 1em;
  width: 100%;
  border-radius: 0.5em;
  margin: 1em 0;
}

@media (max-width: 640px) {
  #chatroom {
    align-items: center;
    margin: 1.2em 1em;
  }

  h1 {
    margin-bottom: 0;
  }

  #chat-div {
    width: 100%;
    max-width: 500px;
    /*max-height: 15em;*/
  }

  button {
    width: 100%;
  }

  .tab {
    margin-left: 1em;
  }
}

@media (min-width: 640px) {
  #chatroom {
    align-items: flex-start;
    width: 100%;
    margin-top: 1em;
    margin-right: 2em;
  }

  #chat-div {
    min-height: 300px;
    min-width: 600px;
    /*max-height: 750px;*/
  }

  button {
    min-width: 10em;
  }
}
</style>
