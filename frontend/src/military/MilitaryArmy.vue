<template>
  <div>
    <div>
      <div id="double-tap-modal">
        <strong>{{ army.name }}</strong>
        <div>
          Attack: {{ army.attack }}
          Defence: {{ army.defence }}
          Type: {{ army.type }}
          Description: {{ army.description }}
        </div>
      </div>
    </div>

    <span v-if="labelsOn">Available: </span> {{ army.available }}
    <span v-if="labelsOn">Away: </span> {{ army.traveling }}
    <span v-if="labelsOn">Training: </span><tool-tip
      :content="army.currentlyTraining"
      :tip="'Max trainable per day: ' + army.trainablePerDay"
      align="left"
    />

    <span v-if="labelsOn">Cost: </span>
    <span>
      <div v-if="isSummon">
        N/A
      </div>
      <span v-else>
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
      </span>
    </span>

    <build-unit-selector />
    <button
      id="submit-button"
      type="submit"
      :disabled="disabled"
    >
      Train
    </button>
  </div>
</template>

<script>
import ToolTip from '@/components/ToolTip.vue'

export default {
  name: 'MilitaryArmy',
  components: {
    ToolTip,
  },
  props: {
    army: Object,
    labelsOn: {
      type: Boolean,
      default: true,
    },
  },
  data () {
    return {
    }
  },
}
</script>
