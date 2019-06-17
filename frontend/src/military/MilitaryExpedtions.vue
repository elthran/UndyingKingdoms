<template>
  <div>
    <h2>Expeditions:</h2>
    <!-- {% for expedition in county.get_expeditions() %}
    <br>
    {% if expedition.success == 0 %}
    Your surviving {{ expedition.peasant + expedition.soldier + expedition.besieger + expedition.summon + expedition.elite + expedition.monster }} troops will
    return in {{ expedition.duration }} days after their failed attack.
    {% elif expedition.mission == 'Attack' %}
    Your surviving {{ expedition.peasant + expedition.soldier + expedition.besieger + expedition.summon + expedition.elite + expedition.monster }} troops will
    return in {{ expedition.duration }} days with {{ expedition.land_acquired }} acres of newly captured land.
    {% elif expedition.mission == 'Raze' %}
    Your surviving {{ expedition.peasant + expedition.soldier + expedition.besieger + expedition.summon + expedition.elite + expedition.monster }} troops will
    return in {{ expedition.duration }} days after razing {{ expedition.land_razed }} acres of enemy land.
    {% elif expedition.mission == 'Pillage' %}
    Your surviving {{ expedition.peasant + expedition.soldier + expedition.besieger + expedition.summon + expedition.elite + expedition.monster }} troops will
    return in {{ expedition.duration }} days with {{ expedition.gold_gained }} gold, {{ expedition.wood_gained }} wood,
    and {{ expedition.iron_gained }} iron.
    {% endif %}
    {% else %}
    You have no troops travelling in foreign lands.
    {% endfor %} -->
  </div>
</template>
