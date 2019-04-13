<script>
export default {
  name: 'PrefixTitle',
  props: {
    title: String
  },
  watch: {
    title () {
      // only used when the title changes after page load
      document.title = this.title + ': ' + document.title.split(': ').pop()
    }
  },
  created () {
    document.title = this.title + ': ' + document.title.split(': ').pop()
  },
  render: function () {
    return ''
  }
}
</script>
