<template>
  <tr>
    <td>{{ title }}</td>
    <td>{{ amount }}</td>
    <td>
      <status-number :number="income" />
      <img
        class="resource_icons"
        :src="icon"
      >
    </td>
    <td>-</td>
    <td>
      <ul>
        <li>
          {{ plural }}: {{ '+\u00a0' + income }} <img
            class="resource_icons"
            :src="icon"
          >
        </li>
      </ul>
    </td>
    <td>-</td>
    <td>{{ description }}</td>
  </tr>
</template>

<script>
import StatusNumber from '@/components/StatusNumber.vue'

export default {
  name: 'EconomySimpleRow',
  props: {
    title: "Somename",
    name: "somename",
    plural: "somenames",
    amount: -1,
    income: -1,
    description: "Example description."
  },
  components: {
    'status-number': StatusNumber
  },
  data () {
    return {
      icon () {
        return '/static/dist/images/' + name + '_icon.jpg'
      }
    }
  }
}
</script>
