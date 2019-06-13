from undyingkingdoms.metadata.metadata import all_armies
from undyingkingdoms.models.exports import Transaction
from undyingkingdoms.models.exports import World


def monsters_buildable(county):
    return county.buildings['lair'].total - \
            county.armies['monster'].total - \
            county.armies['monster'].currently_training


def max_trainable_by_cost(county, army):
    try:
        max_size = min(
            county.gold // army.gold,
            county.wood // army.wood,
            county.iron // army.iron
        )
    except ZeroDivisionError:
        max_size = 50
    if army.name == 'monster':
        return min(
            max_size,
            monsters_buildable(county)
        )
    return max_size


def build_units(county, form):
    world = World.query.get(county.kingdom.world_id)
    total_trained = 0
    transaction = Transaction(county.id, county.day, world.day, "buy")
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

    if county.background == 'Warlord':
        happiness_penalty = 0
    else:
        # You lose 1 happiness for each 0.5% of population you force into military.
        happiness_penalty = (total_trained * 200 // county.population) + 1
    county.happiness -= happiness_penalty
    return
