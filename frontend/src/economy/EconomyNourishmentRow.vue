<template>
  <tr>
    <td>Nourishment</td>
    <td>{{ county.nourishment }}%</td>
    <td>
      <status-number :number="nourishmentChange"></status-number>
    </td>
    <td>-</td>
    <td>-</td>
    <td>-</td>
    <td>The better nourished your people, the healthier they will be.
      Your nourishment decreases by 1% for every 200 unfed people each day.
    </td>
  </tr>
</template>

<script>
export default {
  name: 'EconomyNourishmentRow'
}
</script>
