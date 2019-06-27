<template>
  <div>
    <h2>
      Current Attack Power Available: {{ county.offensiveStrength }}
      <span v-if="hasBesiegers">
        + {{ county.besiegerStrength }} for each enemy fort
      </span>
    </h2>
    <h2>Current Defensive Power: {{ county.defensiveStrength }}</h2>
    <h2>{{ county.availableWorkers }} workers available for training</h2>
  </div>
</template>

<script>
export default {
  name: 'MilitaryStrength',
  props: {
    county: Object,
  },
  data () {
    return {
    }
  },
  computed: {
    hasBesiegers () {
      return this.county.besiegerStrength > 0
    }
  },
}
</script>
