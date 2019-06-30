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
        description='Summoned creatures, bound by magic.',
        ability='None',
        ability_description='None'
    )

    if background == 'Alchemist':
        armies['summon'].class_name = 'iron golem'
        armies['summon'].class_name_plural = 'iron golem'
        armies['summon'].description = 'Iron golems are incredibly well armoured.'
        armies['monster'].category = "Infantry"
        armies['summon'].armour_type = "Plate"
        armies['summon'].attack = 35
        armies['summon'].defence = 30
        armies['summon'].health = 20
        armies['summon'].ability = "None"
        armies['summon'].ability_description = "None."

    elif background == 'Artificer':
        armies['summon'].class_name = 'wooden construct'
        armies['summon'].class_name_plural = 'wooden constructs'
        armies['summon'].description = 'Wooden constructs are a formidable fighting unit'
        armies['monster'].category = "Infantry"
        armies['summon'].armour_type = "Plate"
        armies['summon'].attack = 20
        armies['summon'].defence = 20
        armies['summon'].health = 15
        armies['summon'].ability = "None"
        armies['summon'].ability_description = "None."

    elif background == 'Cleric':
        armies['summon'].class_name = 'cherub'
        armies['summon'].class_name_plural = 'cherubs'
        armies['summon'].description = 'Cherubs fly around the battlefield protecting your other units.'
        armies['monster'].category = "Infantry"
        armies['summon'].armour_type = "Unarmoured"
        armies['summon'].attack = 10
        armies['summon'].defence = 10
        armies['summon'].health = 5
        armies['summon'].ability = "Blessing"
        armies['summon'].ability_description = f"When attacking, your army takes 1% fewer " \
                                               f"casualties for each {armies['summon'].class_name}."

    elif background == 'Diplomat':
        armies['summon'].class_name = 'imp'
        armies['summon'].class_name_plural = 'imps'
        armies['summon'].description = 'Imps are weak and cowardly, but swarm their foe in great numbers.'
        armies['monster'].category = "Infantry"
        armies['summon'].armour_type = "Unarmoured"
        armies['summon'].attack = 2
        armies['summon'].defence = 2
        armies['summon'].health = 1
        armies['summon'].ability = "None"
        armies['summon'].ability_description = "None"

    elif background == 'Druid':
        armies['summon'].class_name = 'treant'
        armies['summon'].class_name_plural = 'treants'
        armies['summon'].description = 'Treants ...'
        armies['monster'].category = "Infantry"
        armies['summon'].armour_type = "Plate"
        armies['summon'].attack = 15
        armies['summon'].defence = 15
        armies['summon'].health = 10
        armies['summon'].ability = "Entangling Roots"
        armies['summon'].ability_description = f"When defending, slow the enemy army's " \
            f"return by 3% per {armies['summon'].class_name}."

    elif background == 'Hierophant':
        armies['summon'].class_name = 'lesser daemon'
        armies['summon'].class_name_plural = 'lesser daemons'
        armies['summon'].description = 'Lesser daemons are strong troops.'
        armies['monster'].category = "Infantry"
        armies['summon'].armour_type = "Unarmoured"
        armies['summon'].attack = 25
        armies['summon'].defence = 25
        armies['summon'].health = 10
        armies['summon'].ability = "None"
        armies['summon'].ability_description = "None"

    elif background == 'Merchant':
        armies['summon'].class_name = 'pixie'
        armies['summon'].class_name_plural = 'pixies'
        armies['summon'].description = 'Pixies are mischievous and difficult to capture.'
        armies['summon'].category = "Infantry"
        armies['summon'].armour_type = "Unarmoured"
        armies['summon'].attack = 4
        armies['summon'].defence = 3
        armies['summon'].health = 1
        armies['summon'].ability = "Steal"
        armies['summon'].ability_description = f"When attacking, each {armies['summon'].class_name} " \
            f"steals up to 50 gold from the enemy county."

    elif background == 'Rogue':
        armies['summon'].class_name = 'shadow wraith'
        armies['summon'].class_name_plural = 'shadow wraiths'
        armies['summon'].description = 'Shadow wraiths are sneaky and potent when attacking.'
        armies['monster'].category = "Infantry"
        armies['summon'].armour_type = "Unarmoured"
        armies['summon'].attack = 15
        armies['summon'].defence = 5
        armies['summon'].health = 10
        armies['summon'].ability = "None"
        armies['summon'].ability_description = "None"

    elif background == 'Warlord':
        armies['summon'].class_name = 'valkyrie'
        armies['summon'].class_name_plural = 'valkyries'
        armies['summon'].description = 'Valkyries are obsessed with combat and are very powerful offensive troops.'
        armies['monster'].category = "Infantry"
        armies['summon'].armour_type = "Unarmoured"
        armies['summon'].attack = 30
        armies['summon'].defence = 5
        armies['summon'].health = 5
        armies['summon'].ability = "No Retreat"
        armies['summon'].ability_description = "Any Valkyries who participate in a failing attack will automatically " \
                                               "die before calculating casualties."

    elif background == 'Wizard':
        armies['summon'].class_name = 'elemental'
        armies['summon'].class_name_plural = 'elementals'
        armies['summon'].description = 'Elementals ...'
        armies['monster'].category = "Infantry"
        armies['summon'].armour_type = "Unarmoured"
        armies['summon'].attack = 15
        armies['summon'].defence = 15
        armies['summon'].health = 8
        armies['summon'].ability = "None"
        armies['summon'].ability_description = "None"

    else:
        raise AttributeError(f'Background {background} is unknown')

    return armies
