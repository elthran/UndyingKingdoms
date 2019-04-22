<template>
  <ul id="crumb-trail">
    <li
      v-for="(crumb, index) in trail"
      :key="index"
    >
      <template v-if="index === last">
        {{ crumb.name }}
      </template>
      <template v-else>
        <a
          :href="crumb.url"
          @click.prevent="$emit('pop-trail', { url: crumb.url, name: crumb.title, level: trail.length-index-1 })"
        >
          {{ crumb.name }}
        </a>
      </template>
      <span class="pad">{{ index !== last ? '&#8594;': '' }}</span>
    </li>
  </ul>
</template>

<script>
export default {
  name: 'CrumbTrail',
  props: {
    trail: {
      type: Array,
      default () {
        return [{name: ''}]
      },
    }
  },
  computed: {
    last () {
      return this.trail.length - 1
    }
  }
}
</script>

<style scoped>
#crumb-trail {
  display: flex;
}

.pad {
  padding-right: 0.3em;
}

@media (max-width: 640px) {
  #crumb-trail {
    flex-direction: column;
  }

  #crumb-trail ol:not(:first-child) {
    margin-left: 1em;
  }
}
</style>
