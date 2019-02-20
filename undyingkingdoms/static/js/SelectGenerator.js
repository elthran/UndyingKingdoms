// vue component as JS.
// This component can set it's own delimiter sytax so I just use Vue default.
Vue.component('select-generator', {
  props: ['options', 'value', 'idName'],
  template: `
    <select
      :id="idName"
      :name="idName"
      :value="value"
      @input="$emit('input', $event.target.value)"
    >
      <option v-for="option in options" :value="option[0]">
      {{ option[1] }}
      </option>
    </select>
  `
});
