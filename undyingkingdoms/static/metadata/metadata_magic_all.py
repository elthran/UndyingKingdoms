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
                                        mana_cost=50,
                                        description='Summon a golem to join your army (Not yet implemented).'),
                  'plague winds': Magic(name='plague winds',
                                        category='timed',
                                        targets='hostile',
                                        known=True,
                                        mana_cost=30,
                                        duration=12,
                                        description='Adds a disease to an enemy county for 12 days. While diseased,'
                                                    'their people die 50% more quickly.'),
                  'verdant growth': Magic(name='verdant growth',
                                          category='aura',
                                          targets='friendly',
                                          known=True,
                                          mana_cost=35,
                                          mana_sustain=5,
                                          description='Pastures produce +50% grain while this spell is in effect.'),
                  'meteor': Magic(name='meteor',
                                  category='self',
                                  targets='hostile',
                                  known=True,
                                  mana_cost=15,
                                  description='A meteor blasts the enemy county, killing a chunk of their populace.')
                  }
