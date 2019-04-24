<template>
  <form
    id="message-input"
    ref="form"
    :action="postUrl"
    @submit.prevent="sendForm"
  >
    <h2>{{ title }}</h2>
    <div v-html="form.csrf" />
    <input
      v-if="titleInput"
      id="title"
      ref="title"
      name="title"
      autofocus
      :maxlength="form.TITLE_SIZE"
      placeholder="Title"
      type="text"
      value=""
      required
    >
    <textarea
      id="content"
      ref="content"
      name="content"
      cols="100"
      rows="10"
      placeholder="Content"
      :maxlength="form.CONTENT_SIZE"
      required
    />
    <button
      id="button"
      type="submit"
    >
      {{ buttonLabel }}
    </button>
  </form>
</template>

<script>
export default {
  name: 'MessageInput',
  props: {
    title: String,
    titleInput: {
      type: Boolean,
      default () {
        return true
      }
    },
    buttonLabel: {
      type: String,
      default () {
        return "Create"
      },
    },
    postUrl: String,
    getUrl: {
      type: String,
      default () {
        return '/api/forum/messaging'
      }
    }
  },
  data () {
    return {
      form: Object
    }
  },
  mounted () {
    this.$hydrate(this.getUrl)
    .then(() => {
      // do something interesting
    })
  },
  methods: {
    sendForm () {
      this.$sendForm(this.$refs.form)
      .then(() => {
        // clear form
        if (this.titleInput) {
          this.$refs.title.value = ''
        }
        this.$refs.content.value = ''
        this.$emit("message-sent")
      })
      .catch((error) => {
        console.log("MessageInput error:", error)
      })
    }
  }
}
</script>

<style scoped>
#message-input {
  display: flex;
  flex-direction: column;
}

#title {
  margin-top: 0.6em;
}

#content {
  margin-top: 0.3em;
  margin-bottom: 1em;
}

@media (min-width: 640px) {
  #button {
    max-width: 22em
  }

  #title {
    max-width: 32em;
  }
}
</style>
