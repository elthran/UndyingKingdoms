<style scoped>
.tooltip-wrapper {
  position: relative;
  display: inline-block;
  border-bottom: 1px dotted #ccc;
  cursor: pointer;
  color: #006080;
}

.tooltip-wrapper:hover .tooltip {
  visibility: visible;
  opacity: 1;
}

.tooltip-wrapper .tooltip {
  visibility: hidden;
  position: absolute;
  /*min-width: 12em;*/
  padding-left: 0.3em !important;
  padding-right: 0.3em !important;
  background-color: #555;
  color: #fff;
  text-align: center;
  padding: 5px 0;
  border-radius: 4px;
  z-index: 1;
  opacity: 0;
  transition: opacity .6s;
}

.tooltip-top {
  bottom: 125%;
  left: 50%;
  margin-left: -6em;
}

.arrow-box-for-top:after {
  top: 100%;
  left: 50%;
  border: solid transparent;
  content: " ";
  height: 0;
  width: 0;
  position: absolute;
  pointer-events: none;
  border-color: rgba(85, 85, 85, 0);
  border-top-color: #555;
  border-width: 10px;
  margin-left: -10px;
}

.tooltip-left {
  top: -5px;
  bottom: auto;
  right: 128%;
}

.arrow-box-for-left:after {
  left: 100%;
  top: 50%;
  border: solid transparent;
  content: " ";
  height: 0;
  width: 0;
  position: absolute;
  pointer-events: none;
  border-color: rgba(85, 85, 85, 0);
  border-left-color: #555;
  border-width: 8px;
  margin-top: -8px;
}

.tooltip-right {
  top: -5px;
  left: 125%;
}

.arrow-box-for-right:after {
  right: 100%;
  top: 50%;
  border: solid transparent;
  content: " ";
  height: 0;
  width: 0;
  position: absolute;
  pointer-events: none;
  border-color: rgba(85, 85, 85, 0);
  border-right-color: #555;
  border-width: 10px;
  margin-top: -10px;
}

.tooltip-bottom {
  top: 135%;
  left: 50%;
  margin-left: -6em;
}

.arrow-box-for-bottom:after {
  bottom: 100%;
  left: 50%;
  border: solid transparent;
  content: " ";
  height: 0;
  width: 0;
  position: absolute;
  pointer-events: none;
  border-color: rgba(85, 85, 85, 0);
  border-bottom-color: #555;
  border-width: 8px;
  margin-left: -8px;
}

.tooltip-mouse {
  /* later modified by js code. */
  top: -5px;
  left: 0;
}

.arrow-box-for-mouse:after {
  /* leaving blank on purpose */
}
</style>

<template>
  <div class="tooltip-wrapper">
    <slot>{{ content }}</slot>
    <span
      ref="tooltip"
      class="tooltip"
      :class="'tooltip-' + align + ' ' + 'arrow-box-for-' + align"
    >
      {{ tip }}
    </span>
  </div>
</template>

<script>
export default {
  name: 'ToolTip',
  props: {
    content: String,
    tip: String,
    align: {
      type: String,
      default: 'bottom',
      validator: function (value) {
        // The value must match one of these strings
        return ['top', 'left', 'right', 'bottom', 'mouse'].indexOf(value) !== -1
      }
    },
    bounder: HTMLUListElement,
  },
  data () {
    return {
    }
  },
  mounted () {
    if (this.align === 'mouse') {
      this.$el.addEventListener('mousemove', this.showTooltip)
    }
  },
  beforeDestroy () {
    this.$el.removeEventListener('mousemove', this.showTooltip)
  },
  methods: {
    showTooltip(e) {
      var tooltip = this.$refs.tooltip
      var bounderRect = this.bounder.getBoundingClientRect()
      var absBounderRight = bounderRect.x + bounderRect.width

      tooltip.style.left =
          (e.pageX + tooltip.clientWidth + 20 < absBounderRight)
              ? (e.pageX - bounderRect.x + 10 + "px")
              : (e.pageX - bounderRect.x - tooltip.clientWidth - 20 + "px");

      var absBounderBottom = bounderRect.y + bounderRect.height
      tooltip.style.top = (e.pageY + tooltip.clientHeight + 10 < absBounderBottom)
          ? (5 + "px")
          : (this.$el.clientHeight - tooltip.clientHeight + "px");
    }
  }
}
</script>
