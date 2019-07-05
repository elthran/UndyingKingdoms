<template lang="pug">
  div.container#pointer(
    @click="toggleOpen"
  )
    div.title
      slot(name="title")
    div(
      :class="isOpen ? 'open': 'closed'"
    )
      hr
      slot
</template>

<script>
export default {
  name: "Collapsible",
  model: {
    prop: 'open',
    event: 'change'
  },
  props: {
    open: {
      type: Boolean,
      default: () => false
    }
  },
  data () {
    return {
      isOpen: this.open,
    }
  },
  methods: {
    toggleOpen () {
      this.isOpen = !this.isOpen
      this.$emit('change', this.isOpen)
    }
  }
}
</script>

<style scoped>
.container {
  margin-top: 0.4em;
  border: 1px solid #ccc;
  box-shadow: outset 0 1px 3px #ddd;
  padding-left: 0.6em;
  border-radius: 5px;
}

.title {
  font-size: 1.5em;
}

.closed {
  display: none;
}

.open {
  display: block;
}

#pointer {
  cursor: pointer;
}
</style>
