<template lang="pug">
  div
    p.bottom-spacer-dot-3.
      You may assign a task to your idle population.
    form(
      ref="form"
      :action="allocateWorkersUrl"
      accept-charset="UTF-8"
    )
      span(v-html="form.csrf_token.html")
      select-generator(
        v-model="goal"
        :options="form.goal.choices"
        :selected="goal"
        :id-name="form.goal.id"
      )
    .top-spacer-dot-3.bottom-spacer-1
      span(v-if="goal == 0").
        Your idle citizens will be forced to work, earning your county an additional {{ overworking }} gold per day.
      span(v-if="goal == 1").
        Your idle citizens will be forced to reclaim overgrown land surrounding your county. You are currently {{ landProduced }} / {{ landToClear }} square meters towards reclaiming an acre. You will advance {{ reclaiming }} square meters each day.
      span(v-if="goal == 2").
        Your idle citizens will be forced to forage for food, gaining enough for {{ foraging }} people each day.
      span(v-if="goal == 3").
        Your idle citizens will be allowed to relax, gaining {{ relaxing }} happiness per day.
</template>

<script>
import SelectGenerator from "@/components/SelectGenerator.vue"

export default {
  name: "IdlePopulationForm",
  components: {
    'select-generator': SelectGenerator
  },
  data () {
    return {
      goal: -1,
      allocateWorkersUrl: "",
      overworking: -1,
      landProduced: -1,
      reclaiming: -1,
      landToClear: -1,
      foraging: -1,
      relaxing: -1,
      form: {
        type: Object,
        csrf_token: Object,
        goal: {
          choices: [Array],  // for some reason using default args this way fixes the linting bug.
          id: ""
        }
      },
      errors: Object
    }
  },
  watch: {
    goal (newVal, oldVal) {
      if (oldVal != -1) {  // ignore watcher until after loading initial data.
        this.$sendForm(this.$refs.form, () => {
          this.$hydrate('/api/infrastructure/idle_population')
        })
      }
    }
  },
  mounted () {
    this.$hydrate('/api/infrastructure/idle_population')
    .then(() => {
      this.$emit('loaded')
    })
  }
}
</script>

<style scoped>
</style>
