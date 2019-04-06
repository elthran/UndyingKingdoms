<template>
  <tr>
    <td>Happiness</td>
    <td>{{ happiness }}%</td>
    <td>
      <status-number :number="happinessChange" />
      <img
        class="resource_icons"
        src="/static/dist/images/heart_icon.jpg"
      >
    </td>
    <td>-</td>
    <td>
      <ul>
        <li>
          Natural: +7 <img
            class="resource_icons"
            src="/static/dist/images/heart_icon.jpg"
          >
        </li>
        <li v-if="areRelaxing">
          Relax: +&nbsp;{{ excessProduction }}
          <img 
            class="resource_icons"
            src="/static/dist/images/heart_icon.jpg"
          >
        </li>
      </ul>
    </td>
    <td>
      <ul>
        <li>
          Taxes: {{ -taxRate }} <img
            class="resource_icons"
            src="/static/dist/images/heart_icon.jpg"
          >
        </li>
      </ul>
      <modifier-list 
        :modifier="happinessMod"
        :race="race"
        :background="background"
        value-icon=""
        img="/static/dist/images/heart_icon.jpg"
      />
    </td>
    <td>
      Happiness affects emigration rate and how productive your workers are. If they become too unhappy,
      they may start to question your rule.
    </td>
  </tr>
</template>

<script>
import StatusNumber from '@/components/StatusNumber.vue'
import ModifierList from '@/components/ModifierList.vue'

export default {
  name: 'EconomyHappinessRow',
  components: {
    'status-number': StatusNumber,
    'modifier-list': ModifierList
  },
  props: {
    update: Boolean
  },
  data () {
    return {
      happiness: -1,
      happinessChange: -1,
      areRelaxing: false,
      excessProduction: -1,
      happinessMod: Object,
      race: "",
      background: "",
      taxRate: -1
    }
  },
  watch: {
    update () {
      this.$hydrate('/api/economy/happiness')
    }
  },
  mounted () {
    this.$hydrate('/api/economy/happiness')
  }
}
</script>
