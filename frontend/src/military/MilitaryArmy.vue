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
    div
      tool-tip(
        content="Attack:"
        :tip="metadata.attack"
        align="right"
        tip-width="10em"
      )
      |  {{ army.attack }}
    div Defence: {{ army.defence }}
    div Type: {{ army.category }}
    div Description: {{ army.description }}
    div
      span(v-if="labelsOn") Available:
      | {{ army.available }}
    div
      span(v-if="labelsOn") Away:
      | {{ army.traveling }}
    div
      span(v-if="labelsOn") Training:
      tool-tip(
        :content="army.currentlyTraining"
        :tip="'Max trainable per day: ' + army.trainablePerDay"
        align="right"
      )

    span(v-if="labelsOn") Cost:
    span
      div(v-if="isSummon") N/A
      span(v-else)
        span(v-if="costsGold")
          span(class="buildingGoldCost") {{ army.gold }}
          resource-icon(type="gold")
        span(v-if="costsWood")
          span(class="buildingWoodCost") {{ army.wood }}
          resource-icon(type="wood")
        span(v-if="costsIron")
          span(class="buildingIronCost") {{ army.iron }}
          resource-icon(type="iron")
        span(v-if="isFree")
          Free
</template>

<script>
import ToolTip from '@/components/ToolTip.vue'
import ResourceIcon from '@/components/ResourceIcon.vue'
import BuildSelector from '@/components/BuildSelector.vue'
import Collapsible from '@/components/Collapsible.vue'

export default {
  name: 'MilitaryArmy',
  components: {
    ToolTip,
    ResourceIcon,
    BuildSelector,
    Collapsible,
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
    costsGold () {
      return this.army.gold > 0
    },
    costsIron () {
      return this.army.iron > 0
    },
    costsWood () {
      return this.army.wood > 0
    },
    isFree () {
      return (this.goldPrice + this.woodPrice + this.ironPrice) == 0
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
    hasAbility () {
      return this.army.ability != "None"
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
