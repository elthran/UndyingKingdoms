<template lang="pug">
  div
    p.bottom-spacer-dot-3.
      You may assign a task to your idle population.
    form(
      ref="form"
      :action="allocateWorkersURL"
      accept-charset="UTF-8"
    )
      select-generator(
        v-model="workingGoal"
        :options="form.goal.choices"
        :selected="workingGoal"
        :id-name="form.goal.id"
      )
    .top-spacer-dot-3.bottom-spacer-1
      span(v-if="isOverworking").
        Your idle citizens will be forced to work, earning your county an additional {{ overworking }} gold per day.
      span(v-if="isProducingLand").
        Your idle citizens will be forced to reclaim overgrown land surrounding your county. You are currently {{ landProduced }} / {{ landToClear }} square meters towards reclaiming an acre. You will advance {{ reclaiming }} square meters each day.
      span(v-if="isForaging").
        Your idle citizens will be forced to forage for food, gaining enough for {{ foraging }} people each day.
      span(v-if="isRelaxing").
        Your idle citizens will be allowed to relax, gaining {{ relaxing }} happiness per day.
</template>

<script>
import http from '@/assets/http-helpers'
import apiPaths from '@/assets/api-paths'

import SelectGenerator from "@/components/SelectGenerator.vue"

export default {
  name: "IdlePopulationForm",
  components: {
    SelectGenerator
  },
  props: {
    goal: Number,
    allocateWorkersURL: String,
    overworking: Number,
    landProduced: Number,
    reclaiming: Number,
    landToClear: Number,
    foraging: Number,
    relaxing: Number,
    form: {
      type: Object,
      goal: {
        type: Object,
        choices: Array,
        id: String
      },
      default () { // required to prevent JS complaining.
        return {
          goal: {
            choices: [],
            id: '',
          },
        }
      },
    },
  },
  data () {
    return {
      workingGoal: -1,  // set in 'goal' watcher ..
    }
  },
  computed: {
    isOverworking () {
      return this.workingGoal == 0
    },
    isProducingLand () {
      return this.workingGoal == 1
    },
    isForaging () {
      return this.workingGoal == 2
    },
    isRelaxing () {
      return this.workingGoal == 3
    },
  },
  watch: {
    goal (newVal, oldVal) {
      this.workingGoal = newVal
    },
    workingGoal (val, oldVal) {
      if (oldVal != -1) {  // ignore watcher until after loading initial data.
        const formData = new FormData(this.$refs.form)
        http.put(apiPaths.infrastructureAllocate(), formData)
        .then(() => {
          // console.log('saving the idle population worked!')
        })
      }
    }
  },
}
</script>

<style scoped>
</style>
