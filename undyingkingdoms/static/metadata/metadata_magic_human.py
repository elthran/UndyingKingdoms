from undyingkingdoms.models.magic import Magic

human_spells = {'population_killer': Magic(name='population_killer',
                                           display_name='incantation of fire',
                                           category='instant',
                                           targets='hostile',
                                           known=True,
                                           mana_cost=15,
                                           output=5,
                                           description='A blasts of fire hits the enemy county, '
                                                       'killing 5% of their populace.'),
                'modify_offensive_power': Magic(name='modify_offensive_power',
                                                display_name='Discipline',
                                                category='aura',
                                                targets='self',
                                                known=True,
                                                mana_cost=5,
                                                mana_sustain=1,
                                                output=0.05,
                                                description='While active, your troops have +5% attack power.')
                }
