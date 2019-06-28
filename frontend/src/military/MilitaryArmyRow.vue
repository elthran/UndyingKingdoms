<template>
  <tr>
    <td>{{ army.name }}</td>
    <td>{{ army.available }}</td>
    <td>{{ army.traveling }}</td>
    <td>
      <tool-tip
        :content="army.currentlyTraining"
        :tip="'Max trainable per day: ' + army.trainablePerDay"
        align="left"
      />
    </td>
    <td>
      <military-unit-selector
        v-model.number="sliderValue"
        :army="army"
        :building="army.building"
        :slider-size="sliderSize"
        :is-monster="isMonster"
        :is-summon="isSummon"
      />
    </td>
    <td>
      <div v-if="isSummon">
        N/A
      </div>
      <div v-else>
        <span v-if="costsGold">
          <span class="buildingGoldCost">{{ army.gold }}</span><resource-icon type="gold" />
        </span>
        <span v-if="costsWood">
          <span class="buildingWoodCost">{{ army.wood }}</span><resource-icon type="wood" />
        </span>
        <span v-if="costsIron">
          <span class="buildingIronCost">{{ army.iron }}</span><resource-icon type="iron" />
        </span>
        <span v-if="isFree">
          Free
        </span>
      </div>
    </td>
    <td>
      <tool-tip
        v-if="isBesieger"
        content="*"
        :tip="metadata.besiegerAttack"
        align="left"
      />
      <div v-else>
        {{ army.attack }}
      </div>
    </td>
    <td>{{ army.defence }}</td>
    <td>
      <tool-tip
        :content="army.health"
        :tip="'Armour type: ' + army.armourType"
        align="right"
      />
    </td>
    <td>{{ army.category }}</td>
    <td>{{ army.description }}</td>
  </tr>
</template>

<script>
import MilitaryUnitSelector from './MilitaryUnitSelector.vue'
import ResourceIcon from '@/components/ResourceIcon.vue'
import ToolTip from '@/components/ToolTip.vue'

export default {
  name: 'MilitaryArmyRow',
  components: {
    MilitaryUnitSelector,
    ResourceIcon,
    ToolTip,
  },
  model: {
    prop: 'resources',
    event: 'change',
  },
  props: {
    army: Object,
    metadata: Object,
    resources: Object,
    reset: Boolean,
  },
  data () {
    return {
      sliderValue: 0,
      resourcesRemaining: this.resources,
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
      return this.army.gold == 0  && this.army.wood == 0 && this.army.iron == 0
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
@media (min-width: 640px) {
}
</style>
