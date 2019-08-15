<template lang="pug">
  div#app
    prefix-title(title="Debug")
    tutorial-interface
    router-view(ref="content")
    nav-bar
</template>

<script>
import NavBar from '@/components/NavBar'
import TutorialInterface from '@/tutorial/TutorialInterface'
// import LoadingComponent from '@/components/LoadingComponent.vue'

export default {
  name: 'App',
  components: {
    NavBar,
    TutorialInterface,
    // LoadingComponent,
  },
  data () {
    return {
      isLoading: true,
    }
  },
  watch: {
    $route (to, from) {
      this.isLoading = true
      this.$emit('refocus')
      this.$nextTick(() => {
        this.focusTop()
      })
    }
  },
  methods: {
    focusTop () {
      window.scrollTo(0,0);
    },
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
    justify-content: flex-end;
  }
}
</style>
