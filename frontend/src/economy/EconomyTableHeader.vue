<style scoped>
.flex-table {
  display: flex;
  width: 100%;
}

th {
  vertical-align: bottom;
  border: 1px solid #ddd;
  padding: 0 0.3em 0.3em;
}

th {
  font-weight: bold;
  vertical-align: middle;
}
</style>

<template>
  <tr class="flex-table">
    <th style="flex-grow:0.25;">
      Topic
    </th>
    <th style="flex-grow:0.25;">
      Current
    </th>
    <th style="flex-grow:0.375;">
      Projected Change
    </th>
    <th style="flex-grow:1;">
      Modifiers
    </th>
    <th style="flex-grow:0.9;">
      Projected Growth
    </th>
    <th style="flex-grow:0.9;">
      Projected Losses
    </th>
    <th style="flex-grow:1.125;">
      Notes
    </th>
  </tr>
</template>

<script>
export default {
  name: 'EconomyTableHeader'
}
</script>