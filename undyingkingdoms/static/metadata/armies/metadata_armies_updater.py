from undyingkingdoms.models.armies import Army


def update_armies(background, armies):
    armies['summon'] = Army(
        name='summon',
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
        description='Summoned creatures, bound by magic.'
    )

    if background == 'Alchemist':
        armies['summon'].class_name = 'iron golem'
        armies['summon'].class_name_plural = 'iron golem'
        armies['summon'].description = 'Iron golems are incredibly well armoured.'
        armies['monster'].category = "Infantry"
        armies['monster'].armour_type = "Plate"

    elif background == 'Artificer':
        armies['summon'].class_name = 'wooden construct'
        armies['summon'].class_name_plural = 'wooden constructs'
        armies['summon'].description = 'Wooden construct ...'
        armies['monster'].category = "Infantry"
        armies['monster'].armour_type = "Plate"

    elif background == 'Cleric':
        armies['summon'].class_name = 'cherub'
        armies['summon'].class_name_plural = 'cherubs'
        armies['summon'].description = 'Cherubs ...'
        armies['monster'].category = "Infantry"
        armies['monster'].armour_type = "Plate"

    elif background == 'Diplomat':
        armies['summon'].class_name = 'imp'
        armies['summon'].class_name_plural = 'imps'
        armies['summon'].description = 'Imps ...'
        armies['monster'].category = "Infantry"
        armies['monster'].armour_type = "Plate"

    elif background == 'Druid':
        armies['summon'].class_name = 'treant'
        armies['summon'].class_name_plural = 'treants'
        armies['summon'].description = 'Treants ...'
        armies['monster'].category = "Infantry"
        armies['monster'].armour_type = "Plate"

    elif background == 'Hierophant':
        armies['summon'].class_name = 'lesser daemon'
        armies['summon'].class_name_plural = 'lesser daemons'
        armies['summon'].description = 'Lesser daemon ...'
        armies['monster'].category = "Infantry"
        armies['monster'].armour_type = "Plate"

    elif background == 'Merchant':
        armies['summon'].class_name = 'fairy'
        armies['summon'].class_name_plural = 'fairies'
        armies['summon'].description = 'Fairies ...'
        armies['monster'].category = "Infantry"
        armies['monster'].armour_type = "Plate"

    elif background == 'Rogue':
        armies['summon'].class_name = 'shadow wraith'
        armies['summon'].class_name_plural = 'shadow wraiths'
        armies['summon'].description = 'Shadow wraith ...'
        armies['monster'].category = "Infantry"
        armies['monster'].armour_type = "Plate"

    elif background == 'Warlord':
        armies['summon'].class_name = 'valkyrie'
        armies['summon'].class_name_plural = 'valkyries'
        armies['summon'].description = 'Valkyrie ...'
        armies['monster'].category = "Infantry"
        armies['monster'].armour_type = "Plate"

    elif background == 'Wizard':
        armies['summon'].class_name = 'elemental'
        armies['summon'].class_name_plural = 'elementals'
        armies['summon'].description = 'Elementals ...'
        armies['monster'].category = "Infantry"
        armies['monster'].armour_type = "Plate"

    else:
        raise AttributeError(f'Background {background} is unknown')

    return armies
