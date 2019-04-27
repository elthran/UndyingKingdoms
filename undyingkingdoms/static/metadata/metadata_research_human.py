from undyingkingdoms.models.technologies import Technology

human_technology = {'civic duty': Technology(name='civic duty',
                                             cost=500,
                                             tier=1,
                                             max_level=1,
                                             description='Reduces upkeep cost of men-at-arms by 10 gold each.'),
                    'economics': Technology(name='economics',
                                            cost=750,
                                            tier=2,
                                            max_level=1,
                                            description='Increases all gold income by 15%.'),
                    'knights templar': Technology(name='knights templar',
                                                  cost=1000,
                                                  tier=2,
                                                  max_level=1,
                                                  description='All knights get +3 attack.'),
                    'trading': Technology(name='trading',
                                          cost=750,
                                          tier=2,
                                          max_level=1,
                                          description='All military units cost 5 less gold to train.')
                    }
