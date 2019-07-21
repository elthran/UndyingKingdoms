from importlib import import_module

from app.serializers.vue_safe import generic_vue_safe
from app.metadata.metadata import all_armies
get_models = lambda: import_module('app.models.exports')


def vue_safe_army(county, army):
    return generic_vue_safe(
        army,
        [
            'gold',
            'wood',
            'iron',
            'available',
            'traveling',
            'currently_training',
            'trainable_per_day',
            'armour_type',
            'total',
            'attack',
            'defence',
            'health',
            'category',
            'description',
            'ability',
            'ability_description',
        ],
        key=army.name,
        name=army.class_name.title(),
        name_plural=army.class_name_plural.title(),
        max_trainable=max_trainable(county, army),
    )


def monsters_buildable(county):
    """Calculate the number of monsters buildable."""
    lair = county.buildings['lair']
    monster = county.armies['monster']
    return lair.total - monster.total - monster.currently_training


def max_trainable(county, army):
    """Calculate the maximum trainable amount of each unit type."""

    try:
        gold_cap = county.gold // army.gold
    except ZeroDivisionError:
        gold_cap = float("Inf")

    try:
        wood_cap = county.wood // army.wood
    except ZeroDivisionError:
        wood_cap = float("Inf")

    try:
        iron_cap = county.iron // army.iron
    except ZeroDivisionError:
        iron_cap = float("Inf")

    max_size = min(
        gold_cap,
        wood_cap,
        iron_cap,
        county.get_available_workers(),
    )

    if army.type == army.MONSTER:
        return min(
            max_size,
            monsters_buildable(county)
        )
    return max_size


def build_units(county, form):
    models = get_models()
    world = models.World.query.get(county.kingdom.world_id)
    total_trained = 0
    transaction = models.Transaction(county.id, county.day, world.day, "buy")
    for army in all_armies:
        if form.data[army] > 0:
            total_trained += form.data[army]
            county.gold -= form.data[army] * county.armies[army].gold
            county.wood -= form.data[army] * county.armies[army].wood
            county.iron -= form.data[army] * county.armies[army].iron
            county.armies[army].currently_training += form.data[army]
            transaction.add_purchase(item_name=army,
                                     item_amount=form.data[army],
                                     gold_per_item=county.armies[army].gold,
                                     wood_per_item=county.armies[army].wood,
                                     iron_per_item=county.armies[army].iron)
    transaction.save()

    if total_trained == 0 or county.background == 'Warlord':
        happiness_penalty = 0
    else:
        # You lose 1 happiness for each 0.5% of population you force into military.
        happiness_penalty = (total_trained * 200 // county.population) + 1
    county.happiness -= happiness_penalty
    return


def troop_sum(expedition):
    return (
            expedition.peasant +
            expedition.soldier +
            expedition.besieger +
            expedition.summon +
            expedition.elite +
            expedition.monster
    )
