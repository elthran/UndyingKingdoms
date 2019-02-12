<template>
  <div id="app">
    <vue-title title="Economy"></vue-title>
    <SideBar>
      <p>Actual content</p>
    </SideBar>
  </div>
</template>

<script>
// import HelloWorld from "./components/HelloWorld.vue"
import SideBar from "./components/SideBar.vue"

export default {
  name: 'app',
  components: {
    // HelloWorld
    SideBar
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
