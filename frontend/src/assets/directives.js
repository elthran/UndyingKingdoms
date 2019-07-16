// Register a global custom directive called `v-focus`
Vue.directive('ready', {
  // When the bound element is inserted into the DOM...
  bind (el) {
    this.ready = false
    this.el.style.visibility = 'hidden'
  },
  update (el) {
    // e.g. Focus the element
    // el.focus()

    // children = this.el.querySelectorAll('v-ready')
    // if all sub components are ready set ready to true
    // when top level ready is tripped show component.
  },
  componentUpdated (el) {
    this.ready = true
    this.el.style.visibility = 'visible'
  },
})
