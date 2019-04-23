from undyingkingdoms.models.magic import Magic

goblin_spells = {'population_killer_tier_1': Magic(name='population_killer_tier_1',
                                                   display_name='green fire',
                                                   category='instant',
                                                   targets='hostile',
                                                   known=True,
                                                   mana_cost=15,
                                                   description='A blasts of green fire hits the enemy county, killing some of their populace.'),
                 'bloodlust': Magic(name='bloodlust',display_name='gfhgf',
                                    category='timed',
                                    targets='self',
                                    known=True,
                                    mana_cost=30,
                                    duration=12,
                                    output=15,
                                    description='While active, your troops have +15% attack power.')
}
