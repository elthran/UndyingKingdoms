<template lang="pug">
  div#tutorial(
    v-if="!tutorial.completed"
    class="invisible"
  )
    div(style="text-align:center;")
      img(:src="tutorial.iconRoute")
      h2 {{ tutorial.advisor }} Advisor
    h2 {{ tutorial.stepDescription }}
    a(
      v-if="tutorial.isClickableStep"
      :href="tutorial.url"
      @click.prevent="next"
    )
      button(style="float:left;width:100px;") Next
</template>

<script>
export default {
  components: {
  },
  props: {
    // advisor: String,
    // isClickableStep: Boolean,
    // completed: Boolean,
    // stepDescription: String,
    // url: String,
  },
  data () {
    return {
      tutorial: {
        advisor: '',
        isClickableStep: null,
        completed: null,
        stepDescription: '',
        url: '',
      }
    }
  },
  computed: {
    iconRoute () {
      return `/static/dist/images/${this.advisor}_advisor.jpg`
    },
  },
  mounted () {
    this.update()
      .then(() => {
        this.$el.classList.remove('invisible')
      })
  },
  methods: {
    next () {
      this.axios.get(this.tutorial.url)
        .then(() => {
          this.update()
        })
    },
    update () {
      return this.$hydrate('/gameplay/tutorial/current')
    },
  },
}
</script>

<style scoped>
#tutorial {
  position: absolute;
  top: 30px;
  right: 0px;
  width: 350px;
  border: solid;
  background: white;
}

h2 {
  margin: 15px 0px 10px 30px;
}
</style>
