from undyingkingdoms.models.magic import Magic

generic_spells = {'inspire': Magic(name='inspire',
                                   category='instant',
                                   targets='self',
                                   known=True,
                                   mana_cost=25,
                                   description='Adds +5 happiness to your county.'),
                  'summon golem': Magic(name='summon golem',
                                        category='instant',
                                        targets='self',
                                        known=True,
                                        mana_cost=35,
                                        description='Summon a golem to join your army (Not yet implemented).'),
                  'plague winds': Magic(name='plague winds',
                                        category='timed',
                                        targets='hostile',
                                        known=True,
                                        mana_cost=5,
                                        duration=12,
                                        description='Add a disease to an enemy county for 12 days.')
                  }
