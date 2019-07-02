<template lang="pug">
  collapsible(
    :title="army.name"
    )
    template(v-slot:title)
      strong {{ army.name }}
      span.right
        build-selector(
          v-model.number="sliderValue"
          :army="army"
          :building="army.building"
          :slider-size="sliderSize"
          :is-monster="isMonster"
          :is-summon="isSummon"
        )
        | {{ sliderValue }}
    army-info(
      :army="army"
      :metadata="metadata"
    )
    army-cost(
      :army="army"
      :is-summon="isSummon"
    )
</template>

<script>
import BuildSelector from '@/components/BuildSelector.vue'
import Collapsible from '@/components/Collapsible.vue'
import ArmyInfo from './ArmyInfo.vue'
import ArmyCost from './ArmyCost.vue'

export default {
  name: 'MilitaryArmy',
  components: {
    BuildSelector,
    Collapsible,
    ArmyInfo,
    ArmyCost,
  },
  model: {
    prop: 'resources',
    event: 'change',
  },
  props: {
    army: Object,
    labelsOn: {
      type: Boolean,
      default: true,
    },
    metadata: Object,
    resources: Object,
    reset: Boolean,
  },
  data () {
    return {
      sliderValue: 0,
      resourcesRemaining: this.resources,
      disabled: false,
    }
  },
  computed: {
    isMonster () {
      return this.army.key === 'monster'
    },
    isSummon () {
      return this.army.key === 'summon'
    },
    isBesieger () {
      return this.army.key === 'besieger'
    },
    goldPrice () {
      return (this.army.gold || 0)
    },
    woodPrice () {
      return (this.army.wood || 0)
    },
    ironPrice () {
      return (this.army.iron || 0)
    },
    sliderSize () {
      var totalGold = this.resources.gold
      var totalWood = this.resources.wood
      var totalIron = this.resources.iron
      var workers = this.resources.workers

      var remaining = Math.max(Math.floor(Math.min(
          (totalGold / this.goldPrice) || 0,
          (totalWood / this.woodPrice) || 0,
          (totalIron / this.ironPrice) || 0,
          workers,
          this.army.maxTrainable - (this.sliderValue || 0),
      )), 0)

      var size = (this.sliderValue || 0) + remaining
      return size
    },
  },
  watch: {
    sliderValue (val, oldVal) {
      this.resourcesRemaining = this.calcResourcesRemaining(val, oldVal)
      this.$emit('change', this.resourcesRemaining)
    },
    reset () {
      this.sliderValue = 0
    },
  },
  mounted () {
    // this.$set(this.army, sliderSize)
  },
  methods: {
    calcResourcesRemaining (val, oldVal) {
      return {
        gold: this.resources.gold - (this.goldPrice * (val - oldVal)),
        wood: this.resources.wood - (this.woodPrice * (val - oldVal)),
        iron: this.resources.iron - (this.ironPrice * (val - oldVal)),
        workers: this.resources.workers - (1 * (val - oldVal))
      }
    },
  },
}
</script>

<style scoped>
.right {
  float: right;
}
</style>
