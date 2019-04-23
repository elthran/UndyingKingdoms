from undyingkingdoms.models.magic import Magic

goblin_spells = {'population_killer': Magic(name='population_killer',
                                            display_name='Green Fire',
                                            category='instant',
                                            targets='hostile',
                                            known=True,
                                            mana_cost=8,
                                            output=3,
                                            description='A blasts of green fire kills 3% of their population.'),
                 'raise_offensive_power': Magic(name='raise_offensive_power',
                                                display_name='Bloodlust',
                                                category='timed',
                                                targets='self',
                                                known=True,
                                                mana_cost=30,
                                                duration=12,
                                                output=0.15,
                                                description='While active, all your troops have +15% attack power.')
                 }
