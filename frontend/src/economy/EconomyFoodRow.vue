<template>
  <tr 
    :value="rations"
    @input="$emit('input', $event.target.value)"
  >
    <td>Food</td>
    <td>{{ grain_stores }}</td>
    <td>
      <status-number :number="grainStorageChange" />
      <img
        class="resource_icons"
        src="/static/dist/images/grain_icon.jpg"
      >
    </td>
    <td>
      Rations:<br>
      <select-generator
        v-model="rations"
        :options="form.rations.choices"
        :selected="rations"
        :id-name="form.rations.id"
      />
      <modifier-list 
        :modifier="food_consumed_mod"
        :race="race"
        :background="background"
      />
    </td>
    <td>
      <ul>
        <li>
          Fields: + {{ producedGrain }} <img
            class="resource_icons"
            src="/static/dist/images/grain_icon.jpg"
          >
        </li>
        <li>
          Pastures: + {{ producedDairy }} <img
            class="resource_icons"
            src="/static/dist/images/dairy_icon.jpg"
          >
        </li>
        <li v-if="isForaging">
          Foraging: + {{ excessProduction }} <img
            class="resource_icons"
            src="/static/dist/images/dairy_icon.jpg"
          >
        </li>
      </ul>
    </td>
    <td>
      <ul>
        <li>To be Eaten: {{ foodEaten }}</li>
      </ul>
    </td>
    <td>
      Excess dairy can not be stored in your granaries. If you do not have enough food, your populace will
      begin to starve.
    </td>
  </tr>
</template>

<script>
import StatusNumber from '@/components/StatusNumber.vue'
import SelectGenerator from '@/components/SelectGenerator.vue'
import ModifierList from '@/components/ModifierList.vue'

export default {
  name: 'EconomyFoodRow',
  components: {
    'status-number': StatusNumber,
    'select-generator': SelectGenerator,
    'modifier-list': ModifierList
  },
  props: {
    update: Boolean
  },
  data () {
    return {
      grain_stores: -1,
      grainStorageChange: -1,
      foodEaten: -1,
      rations: -1,
      race: "",
      background: "",
      food_consumed_mod: Object,
      form: {
        rations: {
          choices: [Array],
          id: ""
        }
      },
      producedGrain: -1,
      producedDairy: -1,
      isForaging: false,
      excessProduction: -1,
      errors: Object
    }
  },
  watch: {
    update () {
      this.$hydrate('/api/economy/food')
    }
  },
  mounted () {
    this.$hydrate('/api/economy/food')
  }
}
</script>
