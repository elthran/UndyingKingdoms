<template>
  <span 
    v-if="number > boundry"
    class="positive"
  >
    {{ posText }}
  </span>
  <span 
    v-else-if="number == boundry"
  >
    {{ neutralText }}
  </span>
  <span 
    v-else
    class="negative"
  >
    {{ negText }}
  </span>
</template>

<script>
export default {
  name: 'ThreeStatusText',
  props: {
    number: Number,
    boundry: {
      type: Number,
      default: 0
    },
    posText: {
      type: String,
      default: 'Positive'
    },
    neutralText: {
      type: String,
      default: 'None'
    },
    negText: {
      type: String,
      default: 'Negative'
    }
  }
}
</script>
