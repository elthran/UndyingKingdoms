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
      id="title"
      autofocus
      :maxlength="form.TITLE_SIZE"
      placeholder="Title"
      type="text"
      value=""
    >
    <textarea
      id="content"
      cols="100"
      rows="10"
      placeholder="Content"
      :maxlength="form.CONTENT_SIZE"
    />
    <button type="submit">
      {{ buttonLabel }}
    </button>
  </form>
</template>

<script>
export default {
  name: 'MessageInput',
  props: {
    title: String,
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
</style>
