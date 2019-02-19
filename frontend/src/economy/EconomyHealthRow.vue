<template>
  <tr>
    <td>Health</td>
    {% if county.health >= 75 %}
    <td style="color:green;">
      {% else %}
    <td style="color:red;">
      {% endif %}
      {{ county.health_terminology.title() }}
    </td>
    {% if county.get_health_change() > 0 %}
    <td style="color:green;">Positive
      {% elif county.get_health_change() == 0 %}
    <td>None
      {% else %}
    <td style="color:red;">Negative
      {% endif %}
    </td>
    <td>-</td>
    <td>-</td>
    <td>-</td>
    <td>The current health of your people. If they become unhealthy, they will die at much greater rates and
      become very susceptible to disease and plague.
    </td>
  </tr>
</template>

<script>
export default {
  name: 'EconomyHealthRow'
}
</script>
