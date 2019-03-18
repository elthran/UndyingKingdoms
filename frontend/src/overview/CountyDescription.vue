<template>
  <h1>The {{ race }} county of {{ name }}, led by {{ title }} {{ leader }} the {{ background }}</h1>
</template>

<script>
export default {
  name: 'CountyDescription',
  data () {
    return {
      race: 'someRace',
      name: 'someName',
      title: 'someTitle',
      leader: 'someLeader',
      background: 'someBackground'
    }
  },
  beforeCreate () {
    this.$getData('/api/overview/county_description', this.$deployData)
  }
}
</script>
