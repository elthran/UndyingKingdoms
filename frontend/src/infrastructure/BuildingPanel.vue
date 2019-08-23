<template lang="pug">
  //- using open by default during testing?
  collapsible.top-spacer-1(
    :open="true"
    @change="updateCollapseState"
  )
    template(v-slot:title)
      div.header
        strong {{ building.name }}
        //- @click.stop does nothing at this time.
        build-input(
          v-model="building.amount"
          :buildable="building"
          :max-size="building.max"
          :hide-bottom="isClosed"
          @click.stop
        )
      //- div.top-spacer-dot-6
      //-   | To Be Built:
      //-   select-generator(
      //-     v-model="building.amount"
      //-     :options="building.buildChoices"
      //-     selected="0"
      //-     :id-name="'amount-' + key"
      //-     :disabled="building.buildChoices.length===1"
      //-     :max="building.max"
      //-   )
        //- max is not yet implemented
    div.top-spacer-dot-6
      | Owned: {{ building.total }}
    div Under Construction: {{ building.pending }}
    div
      | Cost: {{ building.goldCost }}
      img(
        class="resource_icons"
        src="/static/dist/images/gold_icon.jpg"
      )
      | / {{ building.woodCost }}
      img(
        class="resource_icons"
        src="/static/dist/images/wood_icon.jpg"
      )
      | / {{ building.stoneCost }}
      img(
        class="resource_icons"
        src="/static/dist/images/stone_icon.jpg"
      )
    div Workers Employed: {{ building.totalEmployed }} ({{ building.workersEmployed }} each)
    div Description: {{ building.description }}
</template>

<script>
import Collapsible from '@/components/Collapsible'
import BuildInput from '@/components/BuildInput'

export default {
  name: 'BuildingPanel',
  components: {
    Collapsible,
    BuildInput,
  },
  model: {
    prop: 'resources',
    event: 'change',
  },
  props: {
    building: Object,
  },
  data () {
    return {
      isClosed: false,
    }
  },
  methods: {
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
