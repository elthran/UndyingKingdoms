<template>
  <ul>
    <li
      v-if="leaderless"
      class="negative"
    >
      Kingdom is in civil war
    </li>
    <li
      v-else
      class="positive"
    >
      Kingdom is at peace
    </li>
    <li>Land: {{ land }} acres</li>
    <li v-if="day < 0">
      Calendar Day: 0
      <span class="negative">(This age will begin in {{ Math.abs(day) }} hours)</span>
    </li>
    <li v-else>
      Calendar: Day {{ day }} ({{ season }}) --> This test ends on day {{ end }}
    </li>
    <li>Weather: {{ weather }}</li>
  </ul>
</template>

<script>
export default {
  name: 'OverviewBasics',
  data () {
    return {
      leaderless: true,
      day: -1,
      weather: 'weatherType',
      land: -1,
      season: 'seasonType',
      end: -1
    }
  },
  mounted () {
    this.$hydrate('/api/overview/basics')
  }
}
</script>
