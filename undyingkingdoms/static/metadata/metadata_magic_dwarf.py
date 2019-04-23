from undyingkingdoms.models.magic import Magic

dwarf_spells = {'population_killer': Magic(name='population_killer',
                                           display_name='Rune Lightning',
                                           category='instant',
                                           targets='hostile',
                                           known=True,
                                           mana_cost=15,
                                           output=4,
                                           description='A blasts of lightning hits the enemy county, '
                                                       'killing 4% of their populace.'),
                'convert_iron_to_gold': Magic(name='convert_iron_to_gold',
                                              display_name='Rune of Alchemy',
                                              category='instant',
                                              targets='self',
                                              known=True,
                                              mana_cost=5,
                                              description='Instantly turns 10 iron into 100 gold.')
                }
