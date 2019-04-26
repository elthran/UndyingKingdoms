from undyingkingdoms.models.armies import Army


def update_armies(background, armies):

    armies['summon'] = Army(name='summon',
                            class_name='summon',
                            class_name_plural='summons',
                            total=0,
                            trainable_per_day=0,
                            gold=100,
                            iron=100,
                            wood=100,
                            upkeep=0,
                            category='Summoned',
                            attack=5,
                            defence=5,
                            health=5,
                            armour_type='Not implemented',
                            description='Summoned creatures, bound by magic.')

    if background == 'Alchemist':
        armies['summon'].class_name = 'iron golem'
        armies['summon'].class_name_plural = 'iron golem'
        armies['summon'].description = 'Iron golems are incredibly well armoured.'
        armies['monster'].category = "Infantry"
        armies['monster'].armour_type = "Plate"

    elif background == 'Artificer':
        armies['summon'].class_name = 'wood golem'
        armies['summon'].class_name_plural = 'wood golem'
        armies['summon'].description = 'Wood golems are incredibly well armoured.'
        armies['monster'].category = "Infantry"
        armies['monster'].armour_type = "Plate"

    elif background == 'Cleric':
        armies['summon'].class_name = 'holy golem'
        armies['summon'].class_name_plural = 'holy golem'
        armies['summon'].description = 'holy golems are incredibly well armoured.'
        armies['monster'].category = "Infantry"
        armies['monster'].armour_type = "Plate"

    elif background == 'Diplomat':
        armies['summon'].class_name = 'talk golem'
        armies['summon'].class_name_plural = 'talk golem'
        armies['summon'].description = 'talk golems are incredibly well armoured.'
        armies['monster'].category = "Infantry"
        armies['monster'].armour_type = "Plate"

    elif background == 'Druid':
        armies['summon'].class_name = 'tree golem'
        armies['summon'].class_name_plural = 'tree golem'
        armies['summon'].description = 'tree golems are incredibly well armoured.'
        armies['monster'].category = "Infantry"
        armies['monster'].armour_type = "Plate"

    elif background == 'Hierophant':
        armies['summon'].class_name = 'sacrifice golem'
        armies['summon'].class_name_plural = 'sacrifice golem'
        armies['summon'].description = 'sacrifice golems are incredibly well armoured.'
        armies['monster'].category = "Infantry"
        armies['monster'].armour_type = "Plate"

    elif background == 'Merchant':
        armies['summon'].class_name = 'gold golem'
        armies['summon'].class_name_plural = 'gold golem'
        armies['summon'].description = 'gold golems are incredibly well armoured.'
        armies['monster'].category = "Infantry"
        armies['monster'].armour_type = "Plate"

    elif background == 'Rogue':
        armies['summon'].class_name = 'thief golem'
        armies['summon'].class_name_plural = 'thief golem'
        armies['summon'].description = 'thief golems are incredibly well armoured.'
        armies['monster'].category = "Infantry"
        armies['monster'].armour_type = "Plate"

    elif background == 'Warlord':
        armies['summon'].class_name = 'war golem'
        armies['summon'].class_name_plural = 'war golem'
        armies['summon'].description = 'war golems are incredibly well armoured.'
        armies['monster'].category = "Infantry"
        armies['monster'].armour_type = "Plate"

    elif background == 'Wizard':
        armies['summon'].class_name = 'magic golem'
        armies['summon'].class_name_plural = 'magic golem'
        armies['summon'].description = 'magic golems are incredibly well armoured.'
        armies['monster'].category = "Infantry"
        armies['monster'].armour_type = "Plate"

    else:
        raise AttributeError(f'Background {background} is unknown')

    return armies
