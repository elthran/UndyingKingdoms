from undyingkingdoms.models.magic import Magic

dwarf_spells = {'population_killer_tier_1': Magic(name='population_killer_tier_1',
                                                  class_name='rune lightning',
                                                  category='instant',
                                                  targets='hostile',
                                                  known=True,
                                                  mana_cost=15,
                                                  description='A blasts of lightning hits the enemy county, killing some of their populace.'),
                'secrets of alchemy': Magic(name='secrets of alchemy',
                                            category='instant',
                                            targets='self',
                                            known=True,
                                            mana_cost=5,
                                            description='Immediately turns 10 iron into 100 gold.')
                }
