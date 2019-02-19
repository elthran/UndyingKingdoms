<template>
  <tr>
    <td>Iron</td>
    <td>{{ county.iron }}</td>
    {% if county.get_iron_income() >= 0 %}
    <td style="color:green;">
      +
      {% else %}
    </td><td style="color:red;">
      {% endif %}
      {{ county.get_iron_income() }} <img
        class="resource_icons"
        src="/static/images/iron_icon.jpg"
      >
    </td>
    <td>-</td>
    <td>
      <ul>
        <li>
          {{ county.buildings['mine'].class_name_plural.title() }}: + {{ county.get_iron_income() }} <img
            class="resource_icons"
            src="/static/images/iron_icon.jpg"
          >
        </li>
      </ul>
    </td>
    <td>-</td>
    <td>Iron is used to equip powerful soldiers.</td>
  </tr>
</template>

<script>
export default {
  name: 'EconomyIronRow'
}
</script>
