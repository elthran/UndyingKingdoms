<script>
export default {
  name: 'PrefixTitle',
  props: {
    title: String
  },
  created () {
    document.title = this.title + ": " + document.title;
  },
  watch: {
    title () {
      // only used when the title changes after page load
      document.title = this.title + ": " + document.title;
    }
  },
  render: function () {
    return "";
  }
}
</script>
