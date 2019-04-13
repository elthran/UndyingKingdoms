<template>
  <ul>
    <li>
      Coffers: {{ gold }} <img
        class="resource_icons"
        src="/static/dist/images/gold_icon.jpg"
      >
    </li>
    <li>
      Lumber: {{ wood }} <img
        class="resource_icons"
        src="/static/dist/images/wood_icon.jpg"
      >
    </li>
    <li>
      Iron: {{ iron }} <img
        class="resource_icons"
        src="/static/dist/images/iron_icon.jpg"
      >
    </li>
    <li>
      Stone: {{ stone }} <img
        class="resource_icons"
        src="/static/dist/images/stone_icon.jpg"
      >
    </li>
    <li>
      Mana: {{ mana }} <img
        class="resource_icons"
        src="/static/dist/images/mana_icon.jpg"
      >
    </li>
  </ul>
</template>

<script>
export default {
  name: 'OverviewTreasury',
  data () {
    return {
      gold: -1,
      wood: -1,
      iron: -1,
      stone: -1,
      mana: -1
    }
  },
  mounted () {
    this.$hydrate('/api/overview/treasury')
  }
}
</script>
