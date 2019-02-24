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
          {{ descriptiveName }}: {{ '+\u00a0' + income }} <img
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
  components: {
    'status-number': StatusNumber
  },
  props: {
    title: String,
    resourceName: String,
    descriptiveName: String,
    amount: Number,
    income: Number,
    description: String
  },
  computed: {
    icon () {
      return '/static/dist/images/' + this.resourceName + '_icon.jpg'
    }
  }
}
</script>
