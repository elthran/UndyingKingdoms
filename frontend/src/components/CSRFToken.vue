<template>
  <input
    :id="id"
    name="csrf_token"
    type="hidden"
    :value="value"
  >
</template>

<script>
export default {
  name: 'CSRFToken',
  props: {
    id: {
      type: String(),
      default () {
        return "csrf_token"
      }
    },
    value: String(),
  }
}
</script>
