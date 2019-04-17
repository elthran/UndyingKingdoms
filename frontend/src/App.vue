<template>
  <div id="app">
    <prefix-title title="Debug" />
    <!-- magic spacer divs for chatroom, hopefully they don't break anything :P -->
    <div />
    <div />
    <div />
    <router-view ref="content" />
    <nav-bar @refocus="focusTop" />
  </div>
</template>

<script>
import NavBar from '@/components/NavBar.vue'

export default {
  name: 'App',
  components: {
    'nav-bar': NavBar
  },
  data () {
    return {
    }
  },
  watch: {
    $route (to, from) {
      this.$emit('refocus')
    }
  },
  methods: {
    focusTop () {
      window.scrollTo(0,0);
    }
  }
}
</script>

<style scoped>
@media(max-width: 640px) {
  #app {
    display: flex;
    flex-direction: column;
  }
}

@media(min-width: 640px) {
  #app {
    display: flex;
    flex-direction: row-reverse;
    justify-content: space-between;
  }
}
</style>
