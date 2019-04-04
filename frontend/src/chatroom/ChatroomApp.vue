<template>
  <div id="chatroom">
    <prefix-title title="Town Hall" />
    <div id="header">
      <h1>Discussion</h1>
      <toggle-swtich
        v-model="globalChatOn"
        on-label="global"
        off-label="kingdom"
        :checked="globalChatOn"
      />
    </div>
    <div id="chat-div">
      <chat-list :messages="messages" />
    </div>
    <br>
    <csrf-token :value="CSRFToken" />
    <input
      id="content"
      autofocus=""
      class="form-control"
      name="content"
      placeholder="Public to your kingdom"
      required
      type="text"
      :value="message"
    >
    <br><br>
    <button
      id="send"
      type="submit"
      @click="sendMessage()"
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
      CSRFToken: String,
      globalChatOn: Boolean,
      messages: [Array],
      message: '',
      action: '/api/chatroom/update'
    }
  },
  watch: {
    globalChatOn () {
      // Reload chat if toggle button is clicked
      this.debouncedUpdateChat()
    }
  },
  beforeCreate () {
    this.$getData('/api/chatroom/update', this.$deployData)
  },
  async created () {
    const { default: _ } = await import(/* webpackChunkName: "lodash" */ 'lodash')
    this.debouncedUpdateChat = _.debounce(this.updateChat, 500, {leading: false, trailing: true})
  },
  methods: {
    updateChat () {
      this.$sendData(this.$data, this.$deployData)
    },
    async sendMessage () {
      this.$data.updateOnly = false
      this.$sendData(this.$data, (resp, status) => {
          this.message = ''
          this.messages.append(
            {
              time: resp.data[0],
              leader: resp.data[1],
              content: resp.data[2]
            }
          )
            //updateScroll();
        }
      )
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
