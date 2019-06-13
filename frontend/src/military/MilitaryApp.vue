<template>
  <div
    id="military-app"
    class="invisible"
  >
    <prefix-title title="War" />

    <br style="margin-bottom: 2em">
  </div>
</template>

<script>
// import SelectGenerator from '@/components/SelectGenerator.vue'

export default {
  name: 'ResearchApp',
  components: {
    // SelectGenerator,
  },
  data () {
    return {
      loaded: false,

    }
  },
  mounted () {
    this.$hydrate('/api/military/update')
    .then(() => {
      this.$el.classList.remove('invisible')
    })
  },
  methods: {
    updatePage (data) {
      // this.$sendForm(this.$refs.form)
      // .then((data) => {
      //   this.$deployData(data)
      // }).catch((error) => {
      //   console.log(error.debugMessage)
      // })
    }
  }
}
</script>

<style scoped>

</style>
