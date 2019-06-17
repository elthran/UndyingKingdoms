<template>
  <!-- [county.gold // army.gold, county.wood // army.wood, county.iron // army.iron]
        (list | sort)[0] replicates min()-->
  <!-- {% set slider_size = max_trainable_by_cost(county, army) %} -->
  <tr>
    <td>{{ army.name }}</td>
    <td>{{ army.available }}</td>
    <td>{{ army.traveling }}</td>
    <td>
      <div class="tooltip">
        {{ army.currently_training }}<span class="tooltip-text">Max trainable per day: {{ army.trainable_per_day }}</span>
      </div>
    </td>
    <!-- <td>
      {% if army.name == 'monster' %}
        {% set lair = county.buildings['lair'] %}
        {% set lair_name = lair.class_name_plural.title() %}
        <span class="invisible" id="monsterMax">{{ slider_size }}</span>
        {% if monsters_buildable(county) <= 0 %}
          <div class="slide-container">
            <input class="slider" type="range" value="0" min="0" max="{{ slider_size }}" step="1" hidden/>
          </div>
          <span class="display" hidden>0</span>
          <span style="color:red;">Requires more<br>{{ lair_name }}</span>
        {% else %}
          <div class="slide-container">
            <input class="slider" type="range" value="0" min="0" max="{{ slider_size }}" data-monster step="1"/>
          </div>
          <span class="display">0</span>
          <span>
            <span class="tooltip">of {{ lair.total - army.total - army.currently_training }}
              <span class="tooltip-text">Build more {{ lair_name }}</span>
            </span>
          </span>
        {% endif %}
      {% elif army.name == 'summon' %}
        N/A
      {% else %}
        <div class="slide-container">
          <input class="slider" type="range" value="0" min="0" max="{{ slider_size }}" step="1"/>
        </div>
        <span class="display">0</span>
      {% endif %}
      <input class="value" name="{{ army.name }}" value="0" hidden/>
    </td>
    <td>
      {% if army.name == 'summon' %}
        N/A
      {% else %}
        {% if army.gold %}
          <span class="buildingGoldCost">{{ army.gold }}</span><img class="resource_icons" src="/static/images/gold_icon.jpg">
        {% endif %}
        {% if army.wood %}
          <span class="buildingWoodCost">{{ army.wood }}</span><img class="resource_icons" src="/static/images/wood_icon.jpg">
        {% endif %}
        {% if army.iron %}
          <span class="buildingIronCost">{{ army.iron }}</span><img class="resource_icons" src="/static/images/iron_icon.jpg">
        {% endif %}
        {% if army.gold == 0 and army.wood == 0 and army.iron == 0 %}Free{% endif %}
      {% endif %}
    </td> -->
    <td>
      <div v-if="army.key == 'besieger'"
        class="tooltip">
        *<span class="tooltip-text">{{ metadata.besiegerAttack }}</span>
      </div>
      <div v-else>
        {{ army.attack }}
      </div>
    </td>
    <td>{{ army.defence }}</td>
    <td>
      <div class="tooltip">
        {{ army.health }}<span class="tooltip-text">Armour type: {{ army.armourType }}</span>
      </div>
    </td>
    <td>{{ army.category }}</td>
    <td>{{ army.description }}</td>
  </tr>
</template>

<script>
export default {
  name: 'MilitaryArmyRow',
  props: {
    army: Object,
    metadata: Object,
  },
  data () {
    return {
    }
  }
}
</script>
