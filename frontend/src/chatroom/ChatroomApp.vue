<template>
  <div id="chatroom">
    <prefix-title title="Town Hall" />
    <div id="header">
      <h1>Discussion</h1>
      <toggle-swtich
        v-model="globalChatOn"
        on-label="global"
        off-label="kingdom"
      />
    </div>
    <div id="chat-div">
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
      toggleWatcher: null
    }
  },
  computed: {
    filteredMessages () {
      return this.messages.filter((m) => this.globalChatOn ? m.room === 'global' : m.room === 'kingdom')
    },
    lastMessageId () {
      return this.messages.slice(-1).id
    },
  },
  mounted () {
    this.$hydrate('/api/chatroom/update')
    .then(() => {
      this.toggleWatcher = this.$watch('globalChatOn', function () {
        this.updateChat()
      })
    })
  },
  methods: {
    updateChat () {
      console.log('updating chat')
      this.$sendData({
        csrf_token: this.CSRFToken,
        global_chat_on: this.globalChatOn,
        action: '/api/chatroom/update',
      }).catch((error) => { console.log(error) })

      // maybe getting these at the same time will work?
      this.$getData('/api/chatroom/update?last_message_id==' + this.lastMessageId)
      .then((data) => {
        this.messages.concat(data.messages)
      }).catch((error) => { console.log(error) })
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
            //updateScroll();
      })
    }
  }
}

// // Declare some globals
// var chatDiv = document.getElementById("chat-div");
// var pad = 10;
// var scrolled = false;

// // Scroll window to bottom if user hasn't scrolled around.
// function updateScroll() {
//     if (!scrolled) {
//         chatDiv.scrollTop = chatDiv.scrollHeight-chatDiv.clientHeight;
//     }
// }

// // Disabled auto-scrolling if user has scrolled content.
// // Re-enable it if they scroll to the bottom.
// $("#chat-div").on('scroll', function() {
//     if (chatDiv.scrollTop >= chatDiv.scrollHeight-chatDiv.clientHeight) {
//         scrolled = false;
//     } else {
//         scrolled = true;
//     }
// });

// function refocus(selector) {
//     // the next line is required to work around a bug in WebKit (Chrome / Safari)
//     if (!scrolled) {
//         var yOffset = $(selector).offset().top + $(selector).height() + pad;
//         $('html, body').animate({
//             scrollTop: yOffset - window.innerHeight
//         });
//     }
// }

// $("form").submit(function (e) {
//     e.preventDefault();
//     sendMessage();
// });

// function updateChat() {
//     $.ajaxSetup({
//         headers: {"X-CSRF-TOKEN": $("#csrf_token").val()}
//     });

//     $.post("/gameplay/chatroom/", {
//         message: "",
//         updateOnly: true,
//         isGlobal: $("#toggle-switch").prop("checked")
//     }, function (resp, status) {
//         if (status === "success") {
//             $("#csrf_token").val(resp.csrf);
//             $("#chatlist").empty();
//             $.each(resp.data, function (ignore, value) {
//                 $("#chatlist").append(
//                     build_element(value[0], value[1], value[2])
//                 );
//             });
//             updateScroll();
//             refocus("#send");
//         }
//     });
// }

// var clock = {
//     handle: null,
//     run: function () {
//         updateChat();  // run immediately on focus, then every x seconds.
//         return setInterval(updateChat, 5000);
//     }
// };

// // Active update function when the window gains focus.
// $(window).on("focus", function () {
//     clock.handle = clock.run();
// });

// // Stop update function when the window loses focus.
// $(window).on("blur", function () {
//     clearInterval(clock.handle);
// });

// // Pull chat date once page loads
// $(document).ready(() => {
//     updateChat()
// });
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
  }

  h1 {
    margin-bottom: 0;
  }

  #chat-div {
    width: 100%;
    max-width: 500px;
    max-height: 480px;
    overflow-y: auto;
  }

  form {
    width: 100%;
    max-width: 500px;
  }

  input {
    padding: 1em;
    width: 100%;
    border-radius: 0.5em;
    margin-bottom: 0.4em;
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
