<script>
export default {
  name: 'vue-title',
  props: ['title'],
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
