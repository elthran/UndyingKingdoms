<template>
  <tr>
    <td>Lumber</td>
    <td>{{ county.wood }}</td>
    {% if county.get_wood_income() >= 0 %}
    <td style="color:green;">+
      {% else %}
    <td style="color:red;">
      {% endif %}
      {{ county.get_wood_income() }} <img class="resource_icons" src="/static/images/wood_icon.jpg">
    </td>
    <td>-</td>
    <td>
      <ul>
        <li>{{ county.buildings['mill'].class_name_plural.title() }}: + {{ county.get_wood_income() }} <img
          class="resource_icons" src="/static/images/wood_icon.jpg">
        </li>
      </ul>
    </td>
    <td>-</td>
    <td>Lumber is used to build buildings and to equip certain soldiers.</td>
  </tr>
</template>

<script>
export default {
  name: 'EconomyWoodRow'
}
</script>
