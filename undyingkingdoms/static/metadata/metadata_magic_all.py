from undyingkingdoms.models.magic import Magic

generic_spells = {'inspire': Magic(name='inspire',
                                   category='remain_in_play',
                                   known=True,
                                   mana_cost=25,
                                   description='Adds +5 happiness to your county.'),
                  'summon golem': Magic(name='summon golem',
                                        category='summon',
                                        known=True,
                                        mana_cost=35,
                                        description='Summon a golem to join your army (Not yet implemented).'),
                  'plague winds': Magic(name='plague winds',
                                        category='timed',
                                        known=True,
                                        mana_cost=35,
                                        description='Add a disease to an enemy county for 12 days (Not yet implemented).')
                  }
