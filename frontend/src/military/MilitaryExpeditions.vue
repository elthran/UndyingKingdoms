<template>
  <div>
    <h2 class="bottom-spacer-dot-3">
      Expeditions:
    </h2>
    <p
      v-for="expedition in unsucessfulExpeditions"
      :key="expedition"
    >
      Your surviving {{ expedition.troops }} troops will
      return in {{ expedition.duration }} days after their failed attack.
    </p>
    <p
      v-for="expedition in attackExpeditions"
      :key="expedition"
    >
      Your surviving {{ expedition.troops }} troops will
      return in {{ expedition.duration }} days with {{ expedition.landAcquired }} acres of newly captured land.
    </p>
    <p
      v-for="expedition in razeExpeditions"
      :key="expedition"
    >
      Your surviving {{ expedition.troops }} troops will
      return in {{ expedition.duration }} days after razing {{ expedition.landRazed }} acres of enemy land.
    </p>
    <p
      v-for="expedition in razeExpeditions"
      :key="expedition"
    >
      Your surviving {{ expedition.troops }} troops will
      return in {{ expedition.duration }} days with {{ expedition.gold_gained }} gold, {{ expedition.wood_gained }} wood, and {{ expedition.iron_gained }} iron.
    </p>
    <p v-if="noExpeditions">
      You have no troops travelling in foreign lands.
    </p>
  </div>
</template>

<script>
export default {
  name: 'MilitaryExpeditions',
  data () {
    return {
      expeditions: [],
    }
  },
  computed: {
    unsucessfulExpeditions () {
      return this.expeditions.filter((e) => { e.sucess == 0 })
    },
    attackExpeditions () {
      return this.expeditions.filter((e) => { e.mission == "Attack" })
    },
    razeExpeditions () {
      return this.expeditions.filter((e) => { e.mission == "Raze" })
    },
    pillageExpeditions () {
      return this.expeditions.filter((e) => { e.mission == "Pillage" })
    },
    noExpeditions () {
      return this.expeditions.length == 0
    },
  },
  mounted () {
    this.$hydrate('/api/military/expeditions')
    .then(() => {

    })
  }
}
</script>
