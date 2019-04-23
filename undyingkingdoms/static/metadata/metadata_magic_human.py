from undyingkingdoms.models.magic import Magic

human_spells = {'population_killer_tier_1': Magic(name='population_killer_tier_1',
                                                  display_name='incantation of fire',
                                                  category='instant',
                                                  targets='hostile',
                                                  known=True,
                                                  mana_cost=15,
                                                  description='A blasts of fire hits the enemy county, killing some of their populace.'),
                'discipline': Magic(name='discipline',display_name='gfhgf',
                                    category='timed',
                                    targets='self',
                                    known=True,
                                    mana_cost=5,
                                    duration=12,
                                    output=5,
                                    description='While active, your troops have +5% attack power.')
                }
