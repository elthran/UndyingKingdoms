<template lang="pug">
  collapsible(
    @change="updateCollapseState"
  )
    template(v-slot:title)
      div.header
        strong {{ army.name }}
        //- @click.stop does nothing at this time.
        build-input(
          v-model="numOfUnits"
          :army="army"
          :max-size="computedMax"
          :is-summon="isSummon"
          :hide-bottom="isClosed"
          @click.stop
        )
    army-info(
      :army="army"
      :metadata="metadata"
      :is-monster="isMonster"
      :units-queued="numOfUnits"
      :building="army.building"
    )
    army-cost(
      :army="army"
      :is-summon="isSummon"
    )
</template>

<script>
import BuildInput from '@/components/BuildInput.vue'
import Collapsible from '@/components/Collapsible.vue'
import ArmyInfo from './ArmyInfo.vue'
import ArmyCost from './ArmyCost.vue'

export default {
  name: 'MilitaryArmy',
  components: {
    BuildInput,
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
      numOfUnits: 0,
      resourcesRemaining: this.resources,
      disabled: false,
      isClosed: true,
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
    computedMax () {
      var totalGold = this.resources.gold
      var totalWood = this.resources.wood
      var totalIron = this.resources.iron
      var workers = this.resources.workers

      var remaining = Math.max(Math.floor(Math.min(
          (totalGold / this.goldPrice) || 0,
          (totalWood / this.woodPrice) || 0,
          (totalIron / this.ironPrice) || 0,
          workers,
          this.army.maxTrainable - (this.numOfUnits || 0),
      )), 0)

      var size = (this.numOfUnits || 0) + remaining
      return size
    },
  },
  watch: {
    numOfUnits (val, oldVal) {
      this.resourcesRemaining = this.calcResourcesRemaining(val, oldVal)
      this.$emit('change', this.resourcesRemaining)
    },
    reset () {
      this.numOfUnits = 0
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
    updateCollapseState (val) {
      this.isClosed = !val
    },
  },
}
</script>

<style scoped>
.header {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
}
</style>
