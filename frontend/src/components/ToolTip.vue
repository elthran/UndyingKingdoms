<style scoped>
.tooltip {
  position: relative;
  display: inline-block;
  border-bottom: 1px dotted #ccc;
  cursor: help;
  color: #006080;
}

.tooltip:hover .tooltip-text {
  visibility: visible;
  opacity: 1;
}

.tooltip .tooltip-text {
  visibility: hidden;
  position: absolute;
  width: 20em;
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
  margin-left: -10em;
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
  margin-left: -10em;
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
</style>

<template>
  <div class="tooltip">
    {{ content }}
    <span
      class="tooltip-text"
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
        return ['top', 'left', 'right', 'bottom'].indexOf(value) !== -1
      }
    }
  }
}
</script>
