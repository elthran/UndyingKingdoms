<template>
  <div>
    <p>
      Current Attack Power: <strong>{{ county.offensiveStrength }}</strong>
      <span v-if="hasBesiegers">
        + {{ county.besiegerStrength }} for each enemy fort
      </span>
    </p>
    <p>Current Defensive Power: <strong>{{ county.defensiveStrength }}</strong></p>
    <p>
      <strong>{{ county.availableWorkers }}</strong>
      workers available for training
    </p>
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

<style scoped>
p {
  font-size: large;
}
</style>
