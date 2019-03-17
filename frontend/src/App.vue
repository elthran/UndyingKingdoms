<template>
  <div id="app">
    <prefix-title title="Home" />
    <router-view />
    <nav-bar />
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
  }
}
</script>
