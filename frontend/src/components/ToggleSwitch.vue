<template>
  <label class="switch">
    <input
      id="toggle-switch"
      type="checkbox"
      :checked="value"
      @input="$emit('input', $event.target.checked)"
    >
    <div class="slider round">
      <span class="on">{{ onLabel }}</span>
      <span class="off">{{ offLabel }}</span>
    </div>
  </label>
</template>

<script>
export default {
  name: 'ToggleSwitch',
  props: {
    value: {
      type: Boolean,
      required: true,
    },
    onLabel: String,
    offLabel: String
  },
  data () {
    return {

    }
  }
}
</script>

<style scoped>
.switch {
  position: relative;
  display: inline-block;
  width: 130px;
  height: 34px;
}

.switch input {display:none;}

.slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: CornflowerBlue;
  -webkit-transition: .4s;
  transition: .4s;
}

.slider:before {
  position: absolute;
  content: "";
  height: 26px;
  width: 26px;
  left: 4px;
  bottom: 4px;
  background-color: white;
  -webkit-transition: .4s;
  transition: .4s;
}

input:checked + .slider {
  background-color: BlueViolet;
}

input:focus + .slider {
  box-shadow: 0 0 1px #2196F3;
}

input:checked + .slider:before {
  -webkit-transform: translateX(96px);
  -ms-transform: translateX(96px);
  transform: translateX(96px);
}

/*------ ADDED CSS ---------*/
.on
{
  display: none;
}

.on, .off
{
  color: white;
  position: absolute;
  transform: translate(-50%,-50%);
  top: 50%;
  left: 50%;
  font-size: 14px;
  font-family: Verdana, sans-serif;
}

input:checked+ .slider .on
{display: block;}

input:checked + .slider .off
{display: none;}

/*--------- END --------*/

/* Rounded sliders */
.slider.round {
  border-radius: 34px;
}

.slider.round:before {
  border-radius: 50%;
}
</style>
